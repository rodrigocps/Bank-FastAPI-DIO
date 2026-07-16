import random
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from app.core.database import get_db
from app.core.security import get_password_hash, verify_password, create_access_token
from app.models.account import User, Account
from app.schemas.auth import UserCreate, UserResponse, LoginRequest, TokenResponse

router = APIRouter(prefix="/auth", tags=["Auntenticacao"])

@router.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def register_user(user_data: UserCreate, db: AsyncSession = Depends(get_db)):
    # 1. verifica se o usuario ou o email ja existem
    query = select(User).where((User.username == user_data.username) | (User.email == user_data.email))
    result = await db.execute(query)
    if result.scalars().first():
        raise HTTPException(status_code=400, detail="User or email already registered")
    
    # 2. cria o usuario com a senha criptografada
    hashed_password = get_password_hash(user_data.password)
    new_user = User(
        username=user_data.username,
        email=user_data.email,
        hashed_password=hashed_password
    )
    db.add(new_user)
    await db.flush() # salva temporariamente para gerar o ID do usuario
    
    # 3. Cria a conta corrente vinculada automaticamente
    new_account = Account(
        account_number=str(random.randint(10000, 99999)), # Gera um numero ficticio de 5 digitos
        balance=0.00,
        user_id=new_user.id
    )
    db.add(new_account)
    await db.commit()
    await db.refresh(new_user)
    
    return new_user

@router.post("/login", response_model=TokenResponse)
async def login(login_data: LoginRequest, db: AsyncSession = Depends(get_db)):
    # 1. busca o usuario
    result = await db.execute(select(User).where(User.username == login_data.username))
    user = result.scalars().first()
    
    # 2. valida existencia e senha
    if not user or not verify_password(login_data.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Incorrect username or password")
    
    # 3. Gera o token JWT com o "sub" sendo o username
    access_token = create_access_token(data={"sub": user.name})
    return {"access_token": access_token, "token_type": "bearer"}