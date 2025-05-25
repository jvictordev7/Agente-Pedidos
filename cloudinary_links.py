import os
import cloudinary
import cloudinary.uploader
from dotenv import load_dotenv

load_dotenv()

cloudinary.config(
    cloud_name=os.getenv("CLOUDINARY_CLOUD_NAME"),
    api_key=os.getenv("CLOUDINARY_API_KEY"),
    api_secret=os.getenv("CLOUDINARY_API_SECRET"),
    secure=True
)

def upload_imagem_cloudinary(caminho_arquivo, public_id=None):
    try:
        result = cloudinary.uploader.upload(
            caminho_arquivo,
            public_id=public_id,
            folder="pedidos"
        )
        return result["secure_url"]  # Link direto da imagem
    except Exception as e:
        print(f"Erro ao enviar imagem para Cloudinary: {e}")
        return None

# Exemplo de uso:
# url = upload_imagem_cloudinary("CAMINHO/DA/IMAGEM.jpg", public_id="nome_unico")
# print(url)