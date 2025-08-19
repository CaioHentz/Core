from django.urls import path
from galeria.views import index, purchase, sales

urlpatterns = [
    path('', index, name='index'),
    path('purchase/', purchase, name='purchase'),
    path('sales/', sales, name='sales')
]