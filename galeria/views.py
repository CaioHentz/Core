from decimal import Decimal, InvalidOperation

from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404

from .models import Purchase, Sale, Stock, Product


def index(request):
    return render(request, 'galeria/index.html')


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
