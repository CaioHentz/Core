from django.urls import path
from galeria.views import index, purchase, sales, inventory, products, product_create, product_edit

urlpatterns = [
    path('', index, name='index'),
    path('purchase/', purchase, name='purchase'),
    path('sales/', sales, name='sales'),
    path('inventory/', inventory, name='inventory'),
    path('products/', products, name='products'),
    path('products/new/', product_create, name='product_create'),
    path('products/<int:pk>/edit/', product_edit, name='product_edit'),
]
