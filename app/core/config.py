import os

from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    # O Pydantic Settings busca automaticamente essas variaveis no arquivo .env
    SECRET_KEY: str
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    DATABASE_URL: str
    
    class Cofing:
        # Define onde procurar o arquivo de ambiente
        env_file = ".env"
        
# Instaciamos para importar globalmente no projeto
settings = Settings()