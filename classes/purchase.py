class Purchase:
    def __init__(self, inventory):
        self.inventory = inventory
        self.purchases = [] 

    def add_purchase(self, supplier, product, quantity, price):

        purchase_data = {
            "supplier": supplier,
            "product": product,
            "quantity": quantity,
            "price": price
        }
        self.purchases.append(purchase_data)

        self.inventory.add_stock(product, quantity)

        print(f"[COMPRA] {quantity}x '{product}' comprados de '{supplier}' por R${price:.2f}")
