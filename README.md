# Core

Aplicação simples para gestão de estoque, compras e vendas, com um Dashboard que exibe métricas e gráficos usando Chart.js.

## Funcionalidades
- Dashboard:
  - Total de Vendas (somatório de `quantidade * preço` nas vendas)
  - Total de Compras (somatório de `quantidade * preço` nas compras)
  - Produto mais vendido (por quantidade)
  - Lucro Total (`Total Vendas - Total Compras`)
  - Gráfico “Sales vs Purchases” (valores totais)
  - Gráfico “Top Products by Sales Value” (Top 5 por valor vendido)
- Compras (Purchases):
  - Registro de compras com validação de fornecedor e produto existentes
  - Atualização de estoque ao adicionar compras (`Stock.add_stock`)
  - Mensagens de sucesso/erro
  - Exportação de compras para Excel
- Vendas (Sales):
  - Registro de vendas com validação de cliente e produto existentes
  - Checagem de estoque e decremento ao efetivar a venda (`Stock.remove_stock`)
  - Mensagens de sucesso/erro (inclui erro de estoque insuficiente)
  - Exportação de vendas para Excel
- Estoque (Inventory):
  - Listagem do estoque atual com UoM (Unidade de Medida) por produto
  - Busca por produto via parâmetro `q` (ex.: `/inventory/?q=arroz`)
  - Exportação de estoque para Excel
- Produtos:
  - Listagem de produtos
  - Criação de produto
  - Edição de produto
- Clientes:
  - Listagem de clientes
  - Criação de cliente
  - Edição de cliente
- Fornecedores:
  - Listagem de fornecedores
  - Criação de fornecedor
  - Edição de fornecedor
- Autenticação:
  - Registro de usuário (Create Account)
  - Login com autenticação e redirecionamento para o Dashboard
  - Página de registro sem acesso à navegação lateral (aside); exibe somente o logo no topo
- Navegação (UI):
  - Sidebar com grupos “Documents” (Sales, Purchases, Inventory) e “Master Data” (Products, Customers, Suppliers)
  - Indicação de menu ativo por página
- Formatação de números e moeda:
  - Formatação customizada com separador de milhar `.` e decimal `,`
  - Até 3 casas decimais com remoção de zeros à direita
  - Formatação de moeda com prefixo `$`
- Exportações:
  - Geração de planilhas Excel para Sales, Purchases e Inventory (OpenPyXL)

## Tecnologias
- Back-end: Python (Django 5.2.5)
- Front-end: HTML5 e CSS3
- Gráficos: Chart.js via CDN (sem instalar no Python)
- Formatação de números: lógica customizada para milhar e decimais
- Exportação: OpenPyXL para geração de arquivos `.xlsx`

## Requisitos
- Python 3.11+
- Pip
- Virtualenv (opcional)

Dependências Python (arquivo `requirements.txt`):
```
asgiref==3.9.1
Django==5.2.5
dotenv==0.9.9
pygame==2.6.1
python-dotenv==1.1.1
sqlparse==0.5.3
tzdata==2025.2
openpyxl==3.1.5
```

Chart.js é carregado via CDN (não há dependência Python correspondente).

## Como executar

1. Crie e ative um ambiente virtual (opcional, recomendado):
   - Windows:
     ```
     python -m venv venv
     venv\Scripts\activate
     ```
   - Linux/Mac:
     ```
     python -m venv venv
     source venv/bin/activate
     ```

2. Instale dependências:
   ```
   pip install -r requirements.txt
   ```

3. Aplique migrações:
   - Se estiver dentro do diretório `Core/`:
     ```
     python manage.py migrate
     ```
   - Ou a partir da raiz do repositório:
     ```
     python Core/manage.py migrate
     ```

4. Inicie o servidor de desenvolvimento:
   - Se estiver no diretório `Core/`:
     ```
     python manage.py runserver
     ```
   - Ou a partir da raiz do repositório:
     ```
     python Core/manage.py runserver
     ```

5. Acesse:
   ```
   http://127.0.0.1:8000/
   ```

## URLs principais
- Dashboard: `/`
- Sales: `/sales/`
- Purchases: `/purchase/`
- Inventory: `/inventory/`
- Products (list): `/products/`
- Products (create): `/products/new/`
- Products (edit): `/products/<pk>/edit/`
- Customers (list): `/customers/`
- Customers (create): `/customers/new/`
- Customers (edit): `/customers/<pk>/edit/`
- Suppliers (list): `/suppliers/`
- Suppliers (create): `/suppliers/new/`
- Suppliers (edit): `/suppliers/<pk>/edit/`
- Export Sales: `/sales/export/`
- Export Purchases: `/purchase/export/`
- Export Inventory: `/inventory/export/`
- Register: `/register/`
- Login: `/login/`

## Templates
- Layout base: `Core/templates/galeria/base.html`
- Sidebar: `Core/templates/galeria/_sidebar.html`
- Dashboard: `Core/templates/galeria/index.html`
- Compras: `Core/templates/galeria/purchase.html`
- Vendas: `Core/templates/galeria/sales.html`
- Estoque: `Core/templates/galeria/inventory.html`
- Produtos (list): `Core/templates/galeria/products.html`
- Produto (form create/edit): `Core/templates/galeria/product_form.html`
- Clientes (list): `Core/templates/galeria/customers.html`
- Cliente (form create/edit): `Core/templates/galeria/customer_form.html`
- Fornecedores (list): `Core/templates/galeria/suppliers.html`
- Fornecedor (form create/edit): `Core/templates/galeria/supplier_form.html`
- Registro: `Core/templates/galeria/register.html`
- Login: `Core/templates/galeria/login.html`

Observação de UI para registro:
- Em `register.html`, a navegação lateral (aside) é substituída por um cabeçalho fixo com o logo no topo, sem links de navegação.

## Modelos de dados (resumo)
- `Product(name, description, unit_of_measure)`
- `Supplier(name, description)`
- `Customer(name, description)`
- `Stock(product, quantity)`
  - Métodos de classe:
    - `add_stock(product, quantity)`
    - `remove_stock(product, quantity)`
    - `display_stock(product)`
    - `display_all_stock()`
- `Purchase(supplier, product, quantity, price, created_at)`
  - Propriedade: `total = quantity * price`
- `Sale(customer, product, quantity, price, created_at)`
  - Propriedade: `total = quantity * price`

## Exportações (Excel)
- Sales (`/sales/export/`):
  - Colunas: `Date`, `Customer`, `Product`, `Quantity`, `Price (Unit)`, `Total`
  - Ordenação por `created_at`
- Purchases (`/purchase/export/`):
  - Colunas: `Date`, `Supplier`, `Product`, `Quantity`, `Price (Unit)`, `Total`
  - Ordenação por `created_at`
- Inventory (`/inventory/export/`):
  - Colunas: `Product`, `Quantity`, `UoM`
  - Ordenação por `product`

## Dashboard e Chart.js

### Onde está a lógica dos dados
- View: `Core/galeria/views.py`, função `index(request)`:
  - Calcula `total_sales_value`, `total_purchases_value` e `total_profit`.
  - Consolida dados por produto:
    - Quantidade vendida (`sold_qty_map`)
    - Valor vendido (`sold_value_map = quantidade * preço`)
  - Monta os dados dos gráficos:
    - `charts.totals`:
      - `labels = ["Sales", "Purchases"]`
      - `data = [total_sales_value, total_purchases_value]`
    - `charts.topProducts`:
      - `labels = nomes dos produtos (Top 5 por valor)`
      - `data = valores vendidos por produto`

### Como o Chart.js é carregado
No template `Core/templates/galeria/index.html`:
- Inclusão via CDN:
  ```
  <script src="https://cdn.jsdelivr.net/npm/chart.js@4.4.1/dist/chart.umd.min.js"></script>
  ```
- Os dados de gráfico são passados do Django para o front-end usando `json_script`:
  ```
  {{ charts|json_script:"charts-data" }}
  ```
- No JavaScript do template, os dados são lidos em JSON:
  ```js
  const charts = JSON.parse(document.getElementById('charts-data').textContent);
  const totalsLabels = charts.totals?.labels ?? [];
  const totalsData   = (charts.totals?.data ?? []).map(Number);

  const topLabels = charts.topProducts?.labels ?? [];
  const topData   = (charts.topProducts?.data ?? []).map(Number);
  ```

### Inicialização dos gráficos
- Sales vs Purchases (barras):
  - Ticks e tooltips formatados como moeda.
- Top Products by Sales Value (barras):
  - Usa valor vendido por produto (não quantidade).
  - Ticks e tooltips também formatados como moeda.

## Formatação de números e moeda

Para melhorar a legibilidade, foi adotado:
- Separador de milhar: ponto `.`
- Separador decimal: vírgula `,`
- Máximo de 3 casas decimais (zeros à direita são removidos)
- Valores negativos não exibem ponto imediatamente após `-` (ex.: `$-110.000.400`)

Implementação:
- Server-side (view): `Core/galeria/views.py`
  - Função `_fmt_number(dec)` formata valores com `.` e `,`, e trata negativos corretamente.
  - Função `_currency(dec)` prefixa com `$`.
  - Aplica-se às métricas enviadas ao template:
    - `metrics.total_sales`, `metrics.total_purchases`, `metrics.total_profit`
    - `metrics.product_most_sold_qty` (sem `$`, apenas número)

- Client-side (template): `Core/templates/galeria/index.html`
  - Função `fmt(n)` e `fmtCurrency(n)` formatam ticks e tooltips do Chart.js, espelhando a lógica do servidor.

### Personalização
- Símbolo da moeda:
  - Server-side: altere `return f"${_fmt_number(dec)}"` em `_currency`.
  - Client-side: altere `return '$' + fmt(n);` em `fmtCurrency`.
- Caso deseje aplicar a mesma formatação nas páginas de lista (Sales/Purchase), pode-se criar um template filter reutilizável e usar no lugar de `floatformat:-3`.

## Comportamento com dados vazios
- Se não houver vendas ou compras:
  - O gráfico de Totais renderiza com valores 0.
  - O gráfico de Top Products exibe uma barra “No data” com valor 0 para evitar ficar vazio.

## Desenvolvimento
- O servidor de desenvolvimento do Django faz recarregamento automático ao alterar arquivos (`StatReloader`).
- Logs no terminal mostram requisições e status.

## Observações
- Chart.js é carregado via CDN; não é necessário instalar pacotes JavaScript via npm para rodar o dashboard.
- Esta aplicação é para estudos; não utilize o servidor de desenvolvimento em produção.
