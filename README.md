# Core System

O **Core System** é uma aplicação simples para gerenciamento de **estoque, compras e vendas**, desenvolvida como parte de um projeto acadêmico.  
A aplicação conta com uma interface inicial amigável e telas específicas para **Purchase (compras)** e **Sales (vendas)**.

---

## 📌 Funcionalidades
- **Gestão de estoque**: controle da quantidade de produtos.
- **Registro de compras (Purchase)**: adicionar produtos ao estoque.
- **Registro de vendas (Sales)**: registrar vendas e atualizar o estoque.
- **Interface inicial** com acesso às principais funcionalidades.

---

## 🛠️ Tecnologias Utilizadas
- **Front-end**: HTML5 e CSS3  
- **Back-end**: Python/Django  
- **Estilo**: CSS customizado (sem frameworks)

---

## 🚀 Como executar o projeto

### Pré-requisitos
- [Python 3.11+](https://www.python.org/downloads/)  
- [Django 5+](https://www.djangoproject.com/download/)  

### Passo a passo
1. Clone este repositório:
   ```bash
   git clone https://github.com/CaioHentz/Core.git
   cd core-system
   ```

2. Crie um ambiente virtual e ative-o:
   ```bash
   python -m venv venv
   source venv/bin/activate   # Linux/Mac
   venv\Scripts\activate      # Windows
   ```

3. Instale as dependências:
   ```bash
   pip install django
   ```

4. Execute as migrações:
   ```bash
   python manage.py migrate
   ```

5. Inicie o servidor:
   ```bash
   python manage.py runserver
   ```

6. Acesse no navegador:
   ```
   http://127.0.0.1:8000/
   ```

---

👨‍💻 Desenvolvido para estudos de **Python, Django e Front-end**.
