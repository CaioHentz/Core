from galeria.models import Product, Stock, Sale
from decimal import Decimal

class SalesManager:
    def add_sale(self, customer, product_name, quantity, price):
        try:
            product = Product.objects.get(name=product_name)
            stock = product.stock
        except Product.DoesNotExist:
            print(f"[ERRO] Produto '{product_name}' não encontrado.")
            return False

        if stock.quantity < Decimal(str(quantity)):
            print(f"[ERRO] Estoque insuficiente para '{product.name}'. Disponível: {stock.quantity}")
            return False

        # Cria registro de venda
        sale = Sale.objects.create(
            customer=customer,
            product=product,
            quantity=Decimal(str(quantity)),
            price=Decimal(str(price))
        )

        # Atualiza estoque automaticamente
        stock.remove_stock(quantity)
        print(f"[VENDA] {quantity}x '{product.name}' vendidos para '{customer}' por R${price:.2f}")
        return sale
