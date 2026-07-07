from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy.orm import declarative_base
from app.core.config import settings

# 1. Criar o motor assíncrono (engine) utilizando a URL configurada
engine = create_async_engine(
    settings.DATABASE_URL,
    future=True,
    echo=True # Define com True para ver os SQLs gerados no terminal
)

# 2. Criar a fábrica de sessões assincronas
AsyncSessionLocal = async_sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False
)

# 3. Classe Base para que nossos modelos herdem dela
Base = declarative_base()

# 4. Função de dependência (Dependency Injection) para obter a sesão nas rotas
async def get_db():
    async with AsyncSessionLocal() as session:
        try:
            yield session
        finally:
            await session.close() # Garante o fechamento da sessão