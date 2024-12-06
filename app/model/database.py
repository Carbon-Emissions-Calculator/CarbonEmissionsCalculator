from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi

uri = "mongodb+srv://gabrielpascoli:Rp1vkfyHYhCO2tmP@cluster0.2lohh.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"

# Criar o cliente e conectar ao servidor
client = MongoClient(uri, server_api=ServerApi('1'))

# Testar a conexão
try:
    client.admin.command('ping')
    print("Conexão bem-sucedida com o MongoDB!")
except Exception as e:
    print("Erro ao conectar ao MongoDB:", e)

# Referência para o banco de dados
db = client["fastapi_db"]
