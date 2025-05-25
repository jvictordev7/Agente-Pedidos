from sqlalchemy import Column, String, Date, Boolean
from sqlalchemy.orm import declarative_base

Base = declarative_base()

class Pedido(Base):
    __tablename__ = 'pedidos'

    numero_pedido = Column(String(50), primary_key=True, index=True)
    nome = Column(String(255))
    data_entrega = Column(Date)
    categoria = Column(String(100))
    imagem_url = Column(String(500))
    pdf_url = Column(String(500))
    finalizado = Column(Boolean, default=False)