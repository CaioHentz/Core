class Inventory:
    def __init__(self):
        self.stock = {}

    def add_stock(self, product, quantity):
        if product in self.stock:
            self.stock[product] += quantity
        else:
            self.stock[product] = quantity
        print(f"[ESTOQUE] Produto '{product}' atualizado: {self.stock[product]} unidades.")

    def remove_stock(self, product, quantity):
        if product not in self.stock:
            print(f"[ERRO] Produto '{product}' não encontrado no estoque.")
            return False

        if self.stock[product] < quantity:
            print(f"[ERRO] Estoque insuficiente para '{product}'. Disponível: {self.stock[product]}")
            return False

        self.stock[product] -= quantity
        print(f"[ESTOQUE] Produto '{product}' atualizado: {self.stock[product]} unidades.")
        return True
    
    def display_stock(self, product):

        quantity = self.stock.get(product, 0)
        print(f"[CONSULTA] Produto '{product}' em estoque: {quantity} unidades.")
        return quantity

    def display_all_stock(self):

        if not self.stock:
            print("[CONSULTA] Estoque vazio.")
        else:
            print("\n📦 Estoque atual:")
            for product, quantity in self.stock.items():
                print(f"- {product}: {quantity} unidades")
        return self.stock    
