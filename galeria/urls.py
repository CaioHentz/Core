from django.urls import path
from galeria.views import (
    index,
    purchase,
    sales,
    inventory,
    products,
    product_create,
    product_edit,
    customers,
    customer_create,
    customer_edit,
    suppliers,
    supplier_create,
    supplier_edit,
    sales_export,
    purchase_export,
    inventory_export,
)

urlpatterns = [
    path('', index, name='index'),
    path('purchase/', purchase, name='purchase'),
    path('sales/', sales, name='sales'),
    path('inventory/', inventory, name='inventory'),
    path('products/', products, name='products'),
    path('products/new/', product_create, name='product_create'),
    path('products/<int:pk>/edit/', product_edit, name='product_edit'),

    path('customers/', customers, name='customers'),
    path('customers/new/', customer_create, name='customer_create'),
    path('customers/<int:pk>/edit/', customer_edit, name='customer_edit'),

    path('suppliers/', suppliers, name='suppliers'),
    path('suppliers/new/', supplier_create, name='supplier_create'),
    path('suppliers/<int:pk>/edit/', supplier_edit, name='supplier_edit'),

    path('sales/export/', sales_export, name='sales_export'),
    path('purchase/export/', purchase_export, name='purchase_export'),
    path('inventory/export/', inventory_export, name='inventory_export'),
]
