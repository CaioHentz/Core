from django.db import models
from decimal import Decimal
from django.utils import timezone


class Product(models.Model):
    
    name = models.CharField(max_length=25, unique=True)
    description = models.TextField(blank=True)
    unit_of_measure = models.CharField(max_length=25)

    def __str__(self):
        return f"{self.name} ({self.unit_of_measure})"

class Supplier(models.Model):
    name = models.CharField(max_length=25, unique=True)
    description = models.TextField(blank=True)

    def __str__(self):
        return f"{self.name}"

class Customer(models.Model):
    name = models.CharField(max_length=25, unique=True)
    description = models.TextField(blank=True)

    def __str__(self):
        return f"{self.name}"

class Stock(models.Model):
    product = models.CharField(max_length=25, null=False, blank=False)
    quantity = models.DecimalField(max_digits=10, decimal_places=3, null=False, default=Decimal("0"))

    def __str__(self):
        return f"Stock(product={self.product}, quantity={self.quantity})"
  
    @classmethod
    def add_stock(cls, product, quantity):
        qty = Decimal(str(quantity))
        obj, _ = cls.objects.get_or_create(product=product, defaults={"quantity": Decimal("0")})
        obj.quantity = (obj.quantity or Decimal("0")) + qty
        obj.save()
        return obj

    @classmethod
    def remove_stock(cls, product, quantity):
        qty = Decimal(str(quantity))
        try:
            obj = cls.objects.get(product=product)
        except cls.DoesNotExist:
            return False
        if obj.quantity < qty:
            return False
        obj.quantity = obj.quantity - qty
        obj.save()
        return True

    @classmethod
    def display_stock(cls, product):
        try:
            obj = cls.objects.get(product=product)
            return obj.quantity
        except cls.DoesNotExist:
            return Decimal("0")

    @classmethod
    def display_all_stock(cls):
        return {s.product: s.quantity for s in cls.objects.all()}


class Purchase(models.Model):
    supplier = models.CharField(max_length=25)
    product = models.CharField(max_length=25, null=False, blank=False)
    quantity = models.DecimalField(max_digits=10, decimal_places=3, null=False)
    price = models.DecimalField(max_digits=10, decimal_places=3, null=False)
    created_at = models.DateTimeField(default=timezone.now)

    @property
    def total(self):
        return self.quantity * self.price

    def __str__(self):
        return f"Purchase(product={self.product}, qty={self.quantity})"


class Sale(models.Model):
    customer = models.CharField(max_length=25)
    product = models.CharField(max_length=25, null=False, blank=False)
    quantity = models.DecimalField(max_digits=10, decimal_places=3, null=False)
    price = models.DecimalField(max_digits=10, decimal_places=3, null=False)
    created_at = models.DateTimeField(default=timezone.now)

    @property
    def total(self):
        return self.quantity * self.price

    def __str__(self):
        return f"Sale(product={self.product}, qty={self.quantity})"

class User(models.Model):
    username = models.CharField(max_length=25, null=False, blank=False)
    password = models.CharField(max_length=25, null=False, blank=False)

    def __str__(self):
        return f"{self.username}"