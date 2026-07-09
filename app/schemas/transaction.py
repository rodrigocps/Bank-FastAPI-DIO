from pydantic import BaseModel, Field, field_validator
from decimal import Decimal
from datetime import datetime
from app.models.transaction import TransactionType

# Schema de entrada para transacoes
class TransactionCreate(BaseModel):
    type: TransactionType
    amount: Decimal = Field(..., max_digits=12, decimal_places=2)
    
    # Impedir valores negativos e zerados direto na validacao do pydantic
    @field_validator('amount')
    @classmethod
    def amount_must_be_positivie(cls, value: Decimal) -> Decimal:
        if value <= 0:
            raise ValueError("The transaction amount must be greater than zero")
        return value
    
# Schema de saide do extrato
class TransactionResponse(BaseModel):
    id: int
    account_id: int
    type: TransactionType
    amount: Decimal
    created_at: datetime
    
    class Config:
        from_attributes = True