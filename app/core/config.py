from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    # O Pydantic Settings busca automaticamente essas variaveis no arquivo .env
    SECRET_KEY: str
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    DATABASE_URL: str
    
    # class Config: (DEPRECIADO)
    # Define onde procurar o arquivo de ambiente
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8"
    )
        
# Instaciamos para importar globalmente no projeto
settings = Settings()