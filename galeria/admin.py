from django.contrib import admin
from .models import Product, Stock, Purchase, Sale

admin.site.register(Product)
admin.site.register(Stock)
admin.site.register(Purchase)
admin.site.register(Sale)
