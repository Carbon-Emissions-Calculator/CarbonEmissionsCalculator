from fastapi import FastAPI
from app.view.view import router

# Instância do aplicativo FastAPI
app = FastAPI(
    title="Carbon Emissions API",
    description="API para gerenciamento e cálculo de emissões de carbono com MongoDB Atlas",
    version="1.0.0"
)

# Incluindo as rotas
app.include_router(router, prefix="/api/v1")

# Ponto de entrada para rodar o servidor
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="127.0.0.1", port=8000, reload=True)