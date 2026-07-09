from contextlib import asynccontextmanager
from fastapi import FastAPI
from app.core.database import Base, engine
from app.models.account import User, Account
from app.models.transaction import Transaction


# Ferenciado de ciclo de vida
async def lifespan(app: FastAPI):
    # Tudo ANTES do 'yield' roda no "startup" (quando a api inicia)
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    
    yield # A API fica rodando aqui enquanto atende as requisições
    
    # Tudo DEPOIS do 'yiled' rodaria no "shutdown" (quando a api desliga) 

app = FastAPI(
    title="Async Bank API",
    decription="Asynchronous Banking API developed with FastAPI and SQLAlchemy",
    version="1.0.0",
    lifespan=lifespan
)

@app.get("/", tags=["Root"])
async def root():
    return {"message": "Welcome to the Asynchronous Banking API!"}

