from purchase import Purchase
from inventory import Inventory
from sales import Sales

estoque = Inventory()

compras = Purchase(estoque)

compras.add_purchase("Fornecedor A", "Teclado", 10, 50.0)
compras.add_purchase("Fornecedor A", "Computador", 5, 1000.0)

print(estoque.display_stock("Teclado"))


vendas = Sales(estoque)
vendas.add_sale("Cliente João", "Teclado", 2, 100.0)
vendas.add_sale("Cliente João", "Mouse", 2, 100.0)

print(estoque.display_stock("Teclado"))
print(estoque.display_all_stock())


