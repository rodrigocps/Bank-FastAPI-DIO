import enum
from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, Numeric, DateTime, Enum
from sqlalchemy.orm import relationship
from app.core.database import Base

# ---- USER MODEL ----
class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    is_active = Column(Boolean, default=True)

    # Relacionamento de 1 para 1 com account (uselist=False garante isso)
    account = relationship("Account", back_populates="user", uselist=False)
    
# --- ACCOUNT MODEL ---
class Account(Base):
    __tablename__ = "accounts"
    
    id = Column(Integer, primary_key=True, index=True)
    account_number = Column(String, unique=True, index=True, nullable=False)
    balance = Column(Numeric(precision=12, scale=2) default=0.00) # Mantem precisão financeira
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)

    # Relacionamentos
    user = relationship("User", back_populates="account")
    transactions = relationship("Transaction", back_populates="account")
    