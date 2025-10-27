from decimal import Decimal, InvalidOperation
from collections import defaultdict

from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404

from .models import Purchase, Sale, Stock, Product


def index(request):
    # Compute key metrics
    sales_qs = Sale.objects.all()
    purchases_qs = Purchase.objects.all()

    total_sales_value = sum((s.total for s in sales_qs), Decimal("0"))
    total_purchases_value = sum((p.total for p in purchases_qs), Decimal("0"))
    total_profit = total_sales_value - total_purchases_value

    # Aggregate quantities sold per product
    sold_qty_map = defaultdict(Decimal)
    for s in sales_qs:
        try:
            sold_qty_map[s.product] += (s.quantity or Decimal("0"))
        except Exception:
            pass

    if sold_qty_map:
        most_sold_name, most_sold_qty = max(sold_qty_map.items(), key=lambda kv: kv[1])
    else:
        most_sold_name, most_sold_qty = "N/A", Decimal("0")

    # Chart data: Top 5 sold products by quantity
    top_sorted = sorted(sold_qty_map.items(), key=lambda kv: kv[1], reverse=True)[:5]
    top_labels = [name for name, _ in top_sorted]
    top_data = [float(q) for _, q in top_sorted]

    # Chart data: Totals (sales vs purchases)
    totals_labels = ["Sales", "Purchases"]
    totals_data = [float(total_sales_value), float(total_purchases_value)]

    # Formatting helpers: up to 3 decimals (trim trailing zeros) with thousands '.' and decimal ','
    def _fmt_number(dec):
        dec = dec or Decimal("0")
        q = dec.quantize(Decimal("0.001"))
        s = format(q, "f")
        neg = s.startswith("-")
        if "." in s:
            int_part, frac_part = s.split(".")
            frac_part = frac_part.rstrip("0")
        else:
            int_part, frac_part = s, ""
        # remove sign from integer part for grouping
        if neg:
            int_part = int_part.lstrip("-")
        # group thousands with '.'
        int_rev = int_part[::-1]
        grouped_rev = ".".join(int_rev[i:i+3] for i in range(0, len(int_rev), 3))
        grouped = grouped_rev[::-1]
        res = f"{grouped},{frac_part}" if frac_part else grouped
        # avoid '-0' representation
        return f"-{res}" if neg and res != "0" else res

    def _currency(dec):
        return f"${_fmt_number(dec)}"

    context = {
        "metrics": {
            "total_sales": _currency(total_sales_value),
            "total_purchases": _currency(total_purchases_value),
            "total_profit": _currency(total_profit),
            "product_most_sold": most_sold_name,
            "product_most_sold_qty": _fmt_number(most_sold_qty),
        },
        "charts": {
            "topProducts": {"labels": top_labels, "data": top_data},
            "totals": {"labels": totals_labels, "data": totals_data},
        },
    }
    return render(request, "galeria/index.html", context)


def purchase(request):
    if request.method == "POST":
        supplier = (request.POST.get("supplier") or "").strip()
        product = (request.POST.get("product") or "").strip()
        quantity_str = (request.POST.get("quantity") or "").strip()
        price_str = (request.POST.get("price") or "").strip()

        if not supplier or not product or not quantity_str or not price_str:
            messages.error(request, "All fields are required.")
        else:
            try:
                qty = Decimal(quantity_str)
                price = Decimal(price_str)
                if qty <= 0 or price < 0:
                    messages.error(request, "Quantity must be > 0 and price must be >= 0.")
                else:
                    # Validate product existence before recording purchase
                    if not Product.objects.filter(name__iexact=product).exists():
                        messages.error(request, f"Product '{product}' does not exist. Please create it first in Products.")
                    else:
                        Purchase.objects.create(
                            supplier=supplier,
                            product=product,
                            quantity=qty,
                            price=price,
                        )
                        # Update stock 
                        Stock.add_stock(product, qty)
                        messages.success(request, f"Added purchase: {qty} x '{product}' from '{supplier}' at {price}.")
                        return redirect("purchase")
            except InvalidOperation:
                messages.error(request, "Invalid number format for quantity or price.")

    purchases = Purchase.objects.order_by("-created_at")
    products_qs = Product.objects.order_by("name")
    uom_map = {p.name.lower(): p.unit_of_measure for p in products_qs}
    for obj in purchases:
        try:
            obj_uom = uom_map.get(obj.product.lower(), "")
        except AttributeError:
            obj_uom = ""
        setattr(obj, "uom", obj_uom)
    context = {
        "purchases": purchases,
        "products": products_qs,
        "uom_map": uom_map,
    }
    return render(request, "galeria/purchase.html", context)


def sales(request):
    if request.method == "POST":
        customer = (request.POST.get("customer") or "").strip()
        product = (request.POST.get("product") or "").strip()
        quantity_str = (request.POST.get("quantity") or "").strip()
        price_str = (request.POST.get("price") or "").strip()

        if not customer or not product or not quantity_str or not price_str:
            messages.error(request, "All fields are required.")
        else:
            try:
                qty = Decimal(quantity_str)
                price = Decimal(price_str)
                if qty <= 0 or price < 0:
                    messages.error(request, "Quantity must be > 0 and price must be >= 0.")
                else:
                    # Validate product existence before sale
                    if not Product.objects.filter(name__iexact=product).exists():
                        messages.error(request, f"Product '{product}' does not exist. Please create it first in Products.")
                    else:
                        # Attempt to remove stock before creating sale 
                        if Stock.remove_stock(product, qty):
                            Sale.objects.create(
                                customer=customer,
                                product=product,
                                quantity=qty,
                                price=price,
                            )
                            messages.success(request, f"Added sale: {qty} x '{product}' to '{customer}' at {price}.")
                            return redirect("sales")
                        else:
                            messages.error(request, f"Insufficient stock for '{product}'.")
            except InvalidOperation:
                messages.error(request, "Invalid number format for quantity or price.")

    sales_qs = Sale.objects.order_by("-created_at")
    products_qs = Product.objects.order_by("name")
    uom_map = {p.name.lower(): p.unit_of_measure for p in products_qs}
    for obj in sales_qs:
        try:
            obj_uom = uom_map.get(obj.product.lower(), "")
        except AttributeError:
            obj_uom = ""
        setattr(obj, "uom", obj_uom)
    context = {
        "sales": sales_qs,
        "products": products_qs,
        "uom_map": uom_map,
    }
    return render(request, "galeria/sales.html", context)

def inventory(request):
    stocks = Stock.objects.order_by("product")
    products_qs = Product.objects.all()
    uom_map = {p.name.lower(): p.unit_of_measure for p in products_qs}
    for obj in stocks:
        try:
            obj_uom = uom_map.get(obj.product.lower(), "")
        except AttributeError:
            obj_uom = ""
        setattr(obj, "uom", obj_uom)
    context = {
        "stocks": stocks,
    }
    return render(request, "galeria/inventory.html", context)


def products(request):
    products_qs = Product.objects.order_by("name")
    context = {"products": products_qs}
    return render(request, "galeria/products.html", context)


def product_create(request):
    if request.method == "POST":
        name = (request.POST.get("name") or "").strip()
        description = (request.POST.get("description") or "").strip()
        uom = (request.POST.get("unit_of_measure") or "").strip()

        if not name or not uom:
            messages.error(request, "Name and unit of measure are required.")
        elif Product.objects.filter(name__iexact=name).exists():
            messages.error(request, f"Product '{name}' already exists.")
        else:
            Product.objects.create(name=name, description=description, unit_of_measure=uom)
            messages.success(request, f"Product '{name}' created.")
            return redirect("products")

    return render(request, "galeria/product_form.html")


def product_edit(request, pk):
    product = get_object_or_404(Product, pk=pk)

    if request.method == "POST":
        name = (request.POST.get("name") or "").strip()
        description = (request.POST.get("description") or "").strip()
        uom = (request.POST.get("unit_of_measure") or "").strip()

        if not name or not uom:
            messages.error(request, "Name and unit of measure are required.")
        elif Product.objects.filter(name__iexact=name).exclude(pk=pk).exists():
            messages.error(request, f"Product '{name}' already exists.")
        else:
            product.name = name
            product.description = description
            product.unit_of_measure = uom
            product.save()
            messages.success(request, f"Product '{name}' updated.")
            return redirect("products")

    return render(request, "galeria/product_form.html", {"product": product})
