from purchase import Purchase
from inventory import Inventory
from sales import Sales


def runapp():
    estoque = Inventory()
    compras = Purchase(estoque)
    vendas = Sales(estoque)

    continuar = 's'

    while continuar == 's':

        acao = int(input("O que deseja fazer?\n1-Compra\n2-Venda\n"))

        if acao == 1:

            fornecedor = str(input("Fonecedor: "))
            produto = str(input("Produto: "))
            quantidade = float(input("Quantidade: "))
            valor = float(input("Valor: "))

            compras.add_purchase(fornecedor, produto, quantidade, valor)

            print(estoque.display_stock(produto))
        if acao == 2:

            cliente = str(input("Cliente: "))
            produto = str(input("Produto: "))
            quantidade = float(input("Quantidade: "))
            valor = float(input("Valor: "))

            vendas.add_sale(cliente, produto, quantidade, valor)

            print(estoque.display_stock(produto))

        continuar = input("Nova ação? [s/n]")

    print(estoque.display_all_stock())