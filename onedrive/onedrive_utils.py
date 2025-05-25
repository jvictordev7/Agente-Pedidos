import requests
from io import BytesIO
import logging
from urllib.parse import urlparse

def gerar_link_publico(link):
    return link

def is_valid_url(url):
    try:
        result = urlparse(url)
        return all([result.scheme, result.netloc])
    except Exception:
        return False

def enviar_imagem(bot, message, link, resposta):
    if not is_valid_url(link):
        bot.reply_to(message, resposta + "\n[URL da imagem inválida]")
        logging.warning(f"URL inválida fornecida: {link}")
        return

    try:
        response = requests.get(link, timeout=10)
        content_type = response.headers.get('Content-Type', '')
        if response.status_code == 200 and content_type.startswith('image/'):
            bot.send_photo(message.chat.id, BytesIO(response.content), caption=resposta)
            logging.info(f"Imagem enviada com sucesso para chat_id {message.chat.id}")
        else:
            msg = (
                f"{resposta}\n[Imagem não disponível]\n"
                f"Status HTTP: {response.status_code}\n"
                f"Tipo: {content_type}"
            )
            bot.reply_to(message, msg)
            logging.warning(f"Falha ao enviar imagem: Status {response.status_code}, Tipo {content_type}, URL: {link}")
    except requests.exceptions.Timeout:
        bot.reply_to(message, resposta + "\n[Tempo de resposta excedido ao baixar a imagem]")
        logging.error(f"Timeout ao baixar imagem: {link}")
    except Exception as e:
        bot.reply_to(message, resposta + f"\n[Erro ao baixar imagem: {e}]")
        logging.error(f"Erro ao baixar imagem: {link} - {e}")