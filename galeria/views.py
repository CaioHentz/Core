from django.shortcuts import render
from django.http import HttpResponse

def index(request):
    return render(request, 'galeria/index.html')

def purchase(request):
    return render(request, 'galeria/purchase.html')

def sales(request):
    return render(request, 'galeria/sales.html')