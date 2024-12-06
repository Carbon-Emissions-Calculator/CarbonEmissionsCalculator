from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, EmailStr
from typing import List
from uuid import uuid4
from fastapi.middleware.cors import CORSMiddleware

# Criando a aplicação FastAPI
app = FastAPI()

# Configurando o middleware CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Modelo de dados para o usuário
class User(BaseModel):
    id: str  # ID será gerado automaticamente como uma string única
    name: str  # Nome do usuário
    email: EmailStr  # Email válido

# Lista para armazenar os usuários
users_db: List[User] = []

# Rota para criar um novo usuário
@app.post("/users", response_model=User)
def create_user(user: User):
    # Verificar se o email já está em uso
    if any(u.email == user.email for u in users_db):
        raise HTTPException(status_code=400, detail="Email já em uso.")
    user.id = str(uuid4())  # Gerar um ID único
    users_db.append(user)
    return user

# Rota para listar todos os usuários
@app.get("/users", response_model=List[User])
def list_users():
    return users_db

# Rota para obter um único usuário pelo ID
@app.get("/users/{user_id}", response_model=User)
def get_user(user_id: str):
    user = next((u for u in users_db if u.id == user_id), None)
    if user is None:
        raise HTTPException(status_code=404, detail="Usuário não encontrado.")
    return user

# Rota para atualizar um usuário
@app.put("/users/{user_id}", response_model=User)
def update_user(user_id: str, updated_user: User):
    for index, user in enumerate(users_db):
        if user.id == user_id:
            updated_user.id = user_id  # Manter o ID original
            users_db[index] = updated_user
            return updated_user
    raise HTTPException(status_code=404, detail="Usuário não encontrado.")

# Rota para deletar um usuário
@app.delete("/users/{user_id}")
def delete_user(user_id: str):
    global users_db
    users_db = [user for user in users_db if user.id != user_id]
    return {"message": "Usuário deletado com sucesso!"}
