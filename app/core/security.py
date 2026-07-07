from datetime import datetime, timedelta, timezone
import jwt
from passlib.context import CryptContext
from app.core.config import settings

# Configura o contexto do hash de senha com bcrypt
pwd_context = CryptContext(schemas=["bcrypt"], deprecated="auto")

# Função para transformar senha plana em Hash
def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)

# Função para verificar se a senha plana bate com o Hash salvo
def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

# Função para gerar o token JWT com o tempo de expiração
def create_access_token(data: dict) -> str:
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    
# Codifica o token utilizando a chave e algoritmo do .env
    encode_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    return encode_jwt