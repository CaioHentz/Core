from galeria.models import Product, Stock
from decimal import Decimal

class Inventory:
    def add_stock(self, product_name, quantity):
        try:
            product = Product.objects.get(name=product_name)
            stock, _ = Stock.objects.get_or_create(product=product)
            stock.add_stock(quantity)
            print(f"[ESTOQUE] Produto '{product.name}' atualizado: {stock.quantity} unidades.")
        except Product.DoesNotExist:
            print(f"[ERRO] Produto '{product_name}' não encontrado.")
            return False
        return True

    def remove_stock(self, product_name, quantity):
        try:
            product = Product.objects.get(name=product_name)
            stock = product.stock
            if stock.remove_stock(quantity):
                print(f"[ESTOQUE] Produto '{product.name}' atualizado: {stock.quantity} unidades.")
                return True
            else:
                print(f"[ERRO] Estoque insuficiente para '{product.name}'. Disponível: {stock.quantity}")
                return False
        except Product.DoesNotExist:
            print(f"[ERRO] Produto '{product_name}' não encontrado.")
            return False

    def display_stock(self, product_name):
        try:
            product = Product.objects.get(name=product_name)
            print(f"[CONSULTA] Produto '{product.name}' em estoque: {product.stock.quantity} unidades.")
            return product.stock.quantity
        except Product.DoesNotExist:
            print(f"[CONSULTA] Produto '{product_name}' não encontrado.")
            return 0

    def display_all_stock(self):
        stocks = Stock.objects.all()
        if not stocks:
            print("[CONSULTA] Estoque vazio.")
        else:
            print("\n📦 Estoque atual:")
            for stock in stocks:
                print(f"- {stock.product.name}: {stock.quantity} unidades")
        return {s.product.name: s.quantity for s in stocks}
