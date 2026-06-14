from fastapi import FastAPI
from contextlib import asynccontextmanager
from app.routers.cliente import router as cliente_router
from app.routers.os import router as os_router
from app.routers.produtos import router as produto_router
from app.routers.usuario import router as usuario_router
from app.routers.equipamento import router as equipamento_router

@asynccontextmanager
async def lifespan(app: FastAPI):
    print("="*60)
    print("Iniciando a API do Bruno Informática...")
    print("="*60)
    yield
    print("="*60)
    print("Finalizando a API do Bruno Informática...")
    print("="*60)

app = FastAPI(
    title="Bruno API",
    description="API para o projeto de Gerenciamento de Ordens de Serviço - Bruno",
    version="1.0.0",
    lifespan=lifespan
)

app.include_router(cliente_router)
app.include_router(produto_router)
app.include_router(os_router)
app.include_router(usuario_router)
app.include_router(equipamento_router)

@app.get("/")
def read_root():
    return {
        "message": "Bem-vindo à Bruno Informática!",
        "docs_url": "/docs",
        "status": "Online"
    }