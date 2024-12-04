from mongoengine import Document, StringField, connect

# Conectar ao MongoDB
connect(db="fastapi_db", host="localhost", port=27017)

# Modelo de usuário
class User(Document):
    name = StringField(required=True, max_length=100)
    email = StringField(required=True, unique=True)
    password = StringField(required=True, min_length=6)
