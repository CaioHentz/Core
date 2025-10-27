from galeria.models import Product, Stock, Purchase
from decimal import Decimal

class PurchaseManager:
    def add_purchase(self, supplier, product_name, quantity, price):
        try:
            product = Product.objects.get(name=product_name)
        except Product.DoesNotExist:
            print(f"[ERRO] Produto '{product_name}' não encontrado.")
            return False

        # Cria registro de compra
        purchase = Purchase.objects.create(
            supplier=supplier,
            product=product,
            quantity=Decimal(str(quantity)),
            price=Decimal(str(price))
        )

        # Atualiza estoque automaticamente
        product.stock.add_stock(quantity)
        print(f"[COMPRA] {quantity}x '{product.name}' comprados de '{supplier}' por R${price:.2f}")
        return purchase
