from database.db_connection import SessionLocal
from database.models import Pedido

novos_links = {
    "12345": "https://res.cloudinary.com/SEU_CLOUD_NAME/image/upload/v1234567890/pedidos/nome_unico.jpg",
    # Adicione outros pedidos aqui
}

session = SessionLocal()
for numero, novo_link in novos_links.items():
    pedido = session.query(Pedido).filter(Pedido.numero_pedido == numero).first()
    if pedido:
        pedido.imagem_url = novo_link
        print(f"Atualizado pedido {numero} com imagem {novo_link}")
session.commit()
session.close()