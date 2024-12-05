# Importando os módulos necessários do FastAPI
from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware

# Criando a aplicação FastAPI
app = FastAPI()

# Configurando o middleware CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Permitir todas as origens
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Modelo de dados usado para receber os números no POST
class Numbers(BaseModel):
    number1: int  # Primeiro número inteiro
    number2: int  # Segundo número inteiro

# Rota GET para retornar a mensagem "hello world"
@app.get("/")
def read_root():
    """
    Endpoint principal que retorna uma mensagem de saudação.
    """
    return {"message": "Hello World"}  # Resposta no formato JSON

# Rota POST para receber dois números e retornar o produto
@app.post("/multiply")
def multiply_numbers(numbers: Numbers):
    """
    Endpoint que recebe dois números inteiros e retorna o produto deles.
    """
    # Calculando o produto dos dois números
    result = numbers.number1 * numbers.number2
    # Retornando o resultado em formato JSON
    return {"number1": numbers.number1, "number2": numbers.number2, "result": result}

# Para executar, salve este código como um arquivo Python, por exemplo, `main.py`.
# Em seguida, use o comando `uvicorn main:app --reload` no terminal.
# A API estará disponível em `http://127.0.0.1:8000`.
