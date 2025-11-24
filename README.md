# Core

Aplicação simples para gestão de estoque, compras e vendas, com um Dashboard que exibe métricas e gráficos usando Chart.js.

## Funcionalidades
- Gestão de estoque: controle da quantidade disponível por produto.
- Registro de compras (Purchase): adiciona itens ao estoque.
- Registro de vendas (Sales): registra vendas e decrementa o estoque.
- Dashboard com:
  - Total de Vendas (somatório de `quantidade * preço` nas vendas)
  - Total de Compras (somatório de `quantidade * preço` nas compras)
  - Produto mais vendido (por quantidade)
  - Lucro Total (`Total Vendas - Total Compras`)
  - Gráfico “Sales vs Purchases” (valores totais)
  - Gráfico “Top Products by Sales Value” (Top 5 por valor vendido)

## Tecnologias
- Back-end: Python (Django 5.2.5)
- Front-end: HTML5 e CSS3
- Gráficos: Chart.js via CDN (sem instalar no Python)
- Formatação de números: lógica customizada para milhar e decimais

## Requisitos
- Python 3.11+:
- Pip
- Virtualenv (opcional)

Dependências Python (arquivo `requirement.txt`):
```
asgiref==3.9.1
Django==5.2.5
dotenv==0.9.9
pygame==2.6.1
python-dotenv==1.1.1
pywin32==309
sqlparse==0.5.3
tzdata==2025.2
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
- Products: `/products/`

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
