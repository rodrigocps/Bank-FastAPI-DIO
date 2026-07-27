from contextlib import asynccontextmanager
from fastapi import FastAPI
from app.core.database import Base, engine
from app.models.account import User, Account
from app.models.transaction import Transaction
from app.routers import auth, banking


async def lifespan(app: FastAPI):
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    
    yield # A API fica rodando aqui enquanto atende as requisições
    
app = FastAPI(
    title="Async Bank API",
    decription="Asynchronous Banking API developed with FastAPI and SQLAlchemy",
    version="1.0.0",
    lifespan=lifespan
)
app.include_router(auth.router)
app.include_router(banking.router)

@app.get("/", tags=["Root"])
async def root():
    return {"message": "Welcome to the Asynchronous Banking API!"}

