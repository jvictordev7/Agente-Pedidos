# 🤖 Agente-Pedidos

Um bot de pedidos para Telegram, feito em Python, que permite consultar, listar e finalizar pedidos de forma simples e rápida. O bot utiliza banco de dados relacional (MySQL ou SQLite) via SQLAlchemy e pode enviar imagens dos pedidos.

## ✨ Funcionalidades

- 📅 Listar pedidos que vencem hoje, amanhã, na semana ou atrasados
- 🏷️ Resumo por categoria (Bordado, Sublimação, DTF)
- 🔎 Filtrar detalhes por categoria
- 🔢 Buscar pedido por número ou categoria
- ✅ Finalizar pedidos diretamente pelo Telegram
- 🖼️ Envio de imagens dos pedidos (links públicos)

## 🚀 Como usar

1. **Clone o repositório**
    ```sh
    git clone https://github.com/seuusuario/Agente-Pedidos.git
    cd Agente-Pedidos
    ```

2. **Crie e ative o ambiente virtual**
    ```sh
    python -m venv .venv
    .venv\Scripts\activate   # Windows
    # ou
    source .venv/bin/activate  # Linux/Mac
    ```

3. **Instale as dependências**
    ```sh
    pip install -r requirements.txt
    ```

4. **Configure o arquivo `.env`**
    ```
    TELEGRAM_TOKEN=seu_token_aqui
    DATABASE_URL=mysql+mysqlconnector://usuario:senha@localhost:3306/seubanco
    # ou para SQLite:
    # DATABASE_URL=sqlite:///./database.db
    ```

5. **Crie as tabelas e rode o bot**
    ```sh
    python main.py
    ```

6. **No Telegram**
    - 🔍 Procure pelo seu bot (ex: @SeuBotNomeBot)
    - ▶️ Clique em "Iniciar" e siga as opções do menu

## 💬 Comandos disponíveis

- `1` — 📆 Pedidos que vencem essa semana
- `2` — 📅 Pedidos que vencem hoje
- `3` — ⏳ Pedidos que vencem amanhã
- `4` — ⏰ Pedidos atrasados
- `mostrar` — 👁️ Mostra detalhes dos pedidos listados
- `mostrar bordado` — 🧵 Mostra apenas pedidos da categoria Bordado
- `mostrar sublimação` — 🎨 Mostra apenas pedidos da categoria Sublimação
- `mostrar dtf` — 🖨️ Mostra apenas pedidos da categoria DTF
- `finalizar <número do pedido>` — ✅ Finaliza o pedido informado

## 🗂️ Estrutura do projeto

```
📁 Agente-Pedidos/
│
├── 📁 database/
│   ├── 📝 db_connection.py
│   └── 📝 models.py
│
├── 📁 onedrive/
│   └── 📝 onedrive_utils.py
│
├── 📁 telegram_bot/
│   └── 📝 bot.py
│
├── 📝 cloudinary_links.py
├── 📝 main.py
├── 📝 requirements.txt
├── 📝 .env
└── 📝 README.md
```

## ℹ️ Observações

- 👥 O bot pode ser usado por vários usuários ao mesmo tempo.
- 🚫 Não suba o arquivo `.env` nem a pasta `.venv` para o GitHub.
- 🛠️ Para usar com MySQL, instale o driver: `pip install mysql-connector-python`
- 🗃️ Para usar com SQLite, não precisa instalar nada extra.

## 📄 Licença

Este projeto está sob a licença MIT. Veja o arquivo [LICENSE](LICENSE) para mais detalhes.