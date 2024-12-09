from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi

uri = "mongodb+srv://israelcarvalho:7WqtC6RZtPig8S8c@carbon.euagh.mongodb.net/?retryWrites=true&w=majority&appName=carbon"

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
