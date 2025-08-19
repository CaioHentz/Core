class Sales:
    def __init__(self, inventory):
        self.inventory = inventory
        self.sales = []  

    def add_sale(self, customer, product, quantity, price):

        if self.inventory.remove_stock(product, quantity):
            sale_data = {
                "customer": customer,
                "product": product,
                "quantity": quantity,
                "price": price
            }
            self.sales.append(sale_data)
            print(f"[VENDA] {quantity}x '{product}' vendidos para '{customer}' por R${price:.2f}")
