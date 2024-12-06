from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware

# Cria a aplicação FastAPI
app = FastAPI()

# Configurando o middleware CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Permite conexões de qualquer origem
    allow_credentials=True,
    allow_methods=["*"],  # Permite todos os métodos HTTP
    allow_headers=["*"],  # Permite todos os cabeçalhos
)

# Modelo de dados para a multiplicação
class MultiplyRequest(BaseModel):
    number1: int
    number2: int

# Rota inicial
@app.get("/")
def read_root():
    return {"message": "Bem-vindo à API de Multiplicação"}

# Endpoint para multiplicar dois números
@app.post("/multiply")
def multiply_numbers(data: MultiplyRequest):
    return {"result": data.number1 * data.number2}
