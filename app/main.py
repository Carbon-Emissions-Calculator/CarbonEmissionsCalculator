from fastapi import FastAPI
from app.view.view import router

app = FastAPI()

# Incluindo as rotas
app.include_router(router, prefix="/api/v1")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="127.0.0.1", port=8000, reload=True)
