import random
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from app.core.database import get_db
from app.core.security import get_password_hash, verify_password, create_access_token
from app.models.account import User, Account
from app.schemas.auth import UserCreate, UserResponse, TokenResponse

router = APIRouter(prefix="/auth", tags=["Authentication"])

@router.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def register_user(user_data: UserCreate, db: AsyncSession = Depends(get_db)):
    # Verifica se o usuario ou o email ja existem
    query = select(User).where((User.username == user_data.username) | (User.email == user_data.email))
    result = await db.execute(query)
    if result.scalars().first():
        raise HTTPException(status_code=400, detail="User or email already registered")
    
    # Cria o usuario com a senha criptografada
    hashed_password = get_password_hash(user_data.password)
    new_user = User(
        username=user_data.username,
        email=user_data.email,
        hashed_password=hashed_password
    )
    db.add(new_user)
    await db.flush()
    
    # Cria a conta corrente vinculada automaticamente
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
async def login(form_data: OAuth2PasswordRequestForm = Depends(), db: AsyncSession = Depends(get_db)):
    # busca o usuario
    result = await db.execute(select(User).where(User.username == form_data.username))
    user = result.scalars().first()
    
    # valida existencia e senha
    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=401, 
            detail="Incorrect username or password", 
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # Gera o token JWT com o "sub" sendo o username
    access_token = create_access_token(data={"sub": user.username})
    return {"access_token": access_token, "token_type": "bearer"}