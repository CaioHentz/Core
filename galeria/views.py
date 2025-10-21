from decimal import Decimal, InvalidOperation

from django.contrib import messages
from django.shortcuts import render, redirect

from .models import Purchase, Sale, Stock


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
                    Purchase.objects.create(
                        supplier=supplier,
                        product=product,
                        quantity=qty,
                        price=price,
                    )
                    # Update stock (logic from classes/inventory.py)
                    Stock.add_stock(product, qty)
                    messages.success(request, f"Added purchase: {qty} x '{product}' from '{supplier}' at {price}.")
                    return redirect("purchase")
            except InvalidOperation:
                messages.error(request, "Invalid number format for quantity or price.")

    purchases = Purchase.objects.order_by("-created_at")
    context = {
        "purchases": purchases,
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
                    # Attempt to remove stock before creating sale (logic from classes/sales.py + inventory.remove_stock)
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
    context = {
        "sales": sales_qs,
    }
    return render(request, "galeria/sales.html", context)

def inventory(request):
    stocks = Stock.objects.order_by("product")
    context = {
        "stocks": stocks,
    }
    return render(request, "galeria/inventory.html", context)
