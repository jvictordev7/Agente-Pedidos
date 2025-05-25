from telegram_bot import bot
from database.models import Base
from database.db_connection import engine

if __name__ == "__main__":
    print("🛠️ Criando tabelas no banco se não existirem...")
    Base.metadata.create_all(bind=engine)

    print("💬 Iniciando Bot Telegram...")
    bot.run()