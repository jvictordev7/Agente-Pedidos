import telebot
from dotenv import load_dotenv
import os
from datetime import datetime, timedelta
from database.db_connection import SessionLocal
from database.models import Pedido
from onedrive.onedrive_utils import gerar_link_publico, enviar_imagem

load_dotenv()

TOKEN = os.getenv('TELEGRAM_TOKEN')
bot = telebot.TeleBot(TOKEN)

# Armazena o último filtro de pedidos por usuário
ultimos_pedidos = {}

@bot.message_handler(commands=['start'])
def start(message):
    menu = (
        "👋 Olá! Escolha uma opção:\n"
        "1️⃣ Pedidos que vencem essa semana\n"
        "2️⃣ Pedidos que vencem hoje\n"
        "3️⃣ Pedidos que vencem amanhã\n"
        "4️⃣ Pedidos atrasados\n"
        "Ou envie o número do pedido ou uma categoria.\n"
        "Para finalizar um pedido, envie: finalizar <número do pedido>"
    )
    bot.reply_to(message, menu)

@bot.message_handler(func=lambda message: True)
def handle_message(message):
    texto = message.text.strip().lower()
    session = SessionLocal()
    user_id = message.from_user.id

    # Finalizar pedido
    if texto.startswith("finalizar"):
        partes = texto.split()
        if len(partes) == 2 and partes[1].isdigit():
            numero = partes[1]
            pedido = session.query(Pedido).filter(Pedido.numero_pedido == numero).first()
            if pedido:
                pedido.finalizado = True
                session.commit()
                bot.reply_to(message, f"✅ Pedido {numero} finalizado com sucesso!")
            else:
                bot.reply_to(message, f"Pedido {numero} não encontrado.")
        else:
            bot.reply_to(message, "Envie: finalizar <número do pedido>")
        session.close()
        return

    # 1 - Pedidos que vencem essa semana (domingo a domingo)
    if texto in ["1", "pedidos que vencem essa semana"]:
        hoje = datetime.now().date()
        domingo_passado = hoje - timedelta(days=hoje.weekday() + 1) if hoje.weekday() != 6 else hoje
        domingo_que_vem = domingo_passado + timedelta(days=6)
        pedidos = session.query(Pedido).filter(
            Pedido.data_entrega >= domingo_passado,
            Pedido.data_entrega <= domingo_que_vem,
            getattr(Pedido, "finalizado", False) == False
        ).all()
        ultimos_pedidos[user_id] = pedidos
        if pedidos:
            # Conta por categoria
            categorias = {}
            for pedido in pedidos:
                cat = getattr(pedido, "categoria", "Sem categoria")
                categorias[cat] = categorias.get(cat, 0) + 1
            resumo_categorias = ""
            for cat, qtd in categorias.items():
                resumo_categorias += f"- {qtd} {cat}\n"
            bot.reply_to(
                message,
                f"Há {len(pedidos)} pedido(s) que vencem essa semana:\n{resumo_categorias}\n"
                "Digite 'mostrar', 'mostrar bordado', 'mostrar sublimação' ou 'mostrar dtf' para ver detalhes."
            )
        else:
            bot.reply_to(message, "Nenhum pedido vence esta semana.")
        session.close()
        return

    # 2 - Pedidos que vencem hoje
    if texto in ["2", "pedidos que vencem hoje"]:
        hoje = datetime.now().date()
        pedidos = session.query(Pedido).filter(
            Pedido.data_entrega == hoje,
            getattr(Pedido, "finalizado", False) == False
        ).all()
        ultimos_pedidos[user_id] = pedidos
        if pedidos:
            categorias = {}
            for pedido in pedidos:
                cat = getattr(pedido, "categoria", "Sem categoria")
                categorias[cat] = categorias.get(cat, 0) + 1
            resumo_categorias = ""
            for cat, qtd in categorias.items():
                resumo_categorias += f"- {qtd} {cat}\n"
            bot.reply_to(
                message,
                f"Há {len(pedidos)} pedido(s) que vencem hoje:\n{resumo_categorias}\n"
                "Digite 'mostrar', 'mostrar bordado', 'mostrar sublimação' ou 'mostrar dtf' para ver detalhes."
            )
        else:
            bot.reply_to(message, "Nenhum pedido vence hoje.")
        session.close()
        return

    # 3 - Pedidos que vencem amanhã
    if texto in ["3", "pedido que vence amanha", "pedidos que vencem amanhã", "pedidos que vencem amanha"]:
        amanha = datetime.now().date() + timedelta(days=1)
        pedidos = session.query(Pedido).filter(
            Pedido.data_entrega == amanha,
            getattr(Pedido, "finalizado", False) == False
        ).all()
        ultimos_pedidos[user_id] = pedidos
        if pedidos:
            categorias = {}
            for pedido in pedidos:
                cat = getattr(pedido, "categoria", "Sem categoria")
                categorias[cat] = categorias.get(cat, 0) + 1
            resumo_categorias = ""
            for cat, qtd in categorias.items():
                resumo_categorias += f"- {qtd} {cat}\n"
            bot.reply_to(
                message,
                f"Há {len(pedidos)} pedido(s) que vencem amanhã:\n{resumo_categorias}\n"
                "Digite 'mostrar', 'mostrar bordado', 'mostrar sublimação' ou 'mostrar dtf' para ver detalhes."
            )
        else:
            bot.reply_to(message, "Nenhum pedido vence amanhã.")
        session.close()
        return

    # 4 - Pedidos atrasados
    if texto in ["4", "pedidos atrasados"]:
        hoje = datetime.now().date()
        pedidos = session.query(Pedido).filter(
            Pedido.data_entrega < hoje,
            getattr(Pedido, "finalizado", False) == False
        ).all()
        ultimos_pedidos[user_id] = pedidos
        if pedidos:
            categorias = {}
            for pedido in pedidos:
                cat = getattr(pedido, "categoria", "Sem categoria")
                categorias[cat] = categorias.get(cat, 0) + 1
            resumo_categorias = ""
            for cat, qtd in categorias.items():
                resumo_categorias += f"- {qtd} {cat}\n"
            bot.reply_to(
                message,
                f"Há {len(pedidos)} pedido(s) atrasados:\n{resumo_categorias}\n"
                "Digite 'mostrar', 'mostrar bordado', 'mostrar sublimação' ou 'mostrar dtf' para ver detalhes."
            )
        else:
            bot.reply_to(message, "Nenhum pedido atrasado.")
        session.close()
        return

    # Mostrar detalhes dos últimos pedidos consultados, com filtro por categoria
    if texto.startswith("mostrar"):
        pedidos = ultimos_pedidos.get(user_id, [])
        if not pedidos:
            bot.reply_to(message, "Nenhum pedido para mostrar.")
            session.close()
            return

        # Filtro por categoria se solicitado
        filtro = texto.replace("mostrar", "").strip().capitalize()
        pedidos_filtrados = pedidos
        if filtro in ["Bordado", "Sublimação", "Dtf"]:
            pedidos_filtrados = [p for p in pedidos if getattr(p, "categoria", "").lower() == filtro.lower()]

        if not pedidos_filtrados:
            bot.reply_to(message, f"Nenhum pedido para mostrar na categoria {filtro}.")
            session.close()
            return

        # Detalhes dos pedidos filtrados (sem resumo)
        for pedido in pedidos_filtrados:
            resposta = (
                f"📦 Pedido: {pedido.numero_pedido}\n"
                f"👕 Nome: {pedido.nome}\n"
                f"🗓️ Entrega: {pedido.data_entrega}\n"
                f"🏷️ Categoria: {getattr(pedido, 'categoria', 'Sem categoria')}\n"
                f"Para finalizar este pedido, envie: finalizar {pedido.numero_pedido}"
            )
            if hasattr(pedido, "imagem_url") and pedido.imagem_url:
                link_direto = gerar_link_publico(pedido.imagem_url)
                enviar_imagem(bot, message, link_direto, resposta)
            else:
                bot.reply_to(message, resposta)
        session.close()
        return

    # Busca por número ou categoria
    if texto.isnumeric():
        pedido = session.query(Pedido).filter(Pedido.numero_pedido == texto).first()
    else:
        pedido = session.query(Pedido).filter(Pedido.categoria == texto).first()

    if pedido:
        resposta = (
            f"📦 Pedido: {pedido.numero_pedido}\n"
            f"👕 Nome: {pedido.nome}\n"
            f"🗓️ Entrega: {pedido.data_entrega}\n"
            f"🏷️ Categoria: {getattr(pedido, 'categoria', 'Sem categoria')}\n"
            f"Para finalizar este pedido, envie: finalizar {pedido.numero_pedido}"
        )
        if hasattr(pedido, "imagem_url") and pedido.imagem_url:
            link_direto = gerar_link_publico(pedido.imagem_url)
            enviar_imagem(bot, message, link_direto, resposta)
        else:
            bot.reply_to(message, resposta)

        if hasattr(pedido, "pdf_url") and pedido.pdf_url:
            bot.send_document(message.chat.id, pedido.pdf_url)
        session.close()
        return

    bot.reply_to(message, "Desculpe, não entendi. Por favor, escolha uma opção do menu ou envie o número do pedido ou uma categoria.")
    session.close()

def run():
    bot.infinity_polling()