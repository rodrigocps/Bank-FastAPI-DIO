from pydantic import BaseModel, EmailStr

# Schema para criacao de usuario (entrada)
class UserCreate(BaseModel):
    username: str
    email: EmailStr
    password: str
    
# Schema de resposta de usuario (saida protegendo a senha)
class UserResponse(BaseModel):
    id: int
    username: str
    email: str
    is_active: bool
    
    class Config:
        from_attributes = True
        
# Schema para capturar dados de login
class LoginRequest(BaseModel):
    username: str
    password: str
    
# Schema do token retornado apos login bem sucedido
class TokenResponse(BaseModel):
    access_token: str
    token_type: str