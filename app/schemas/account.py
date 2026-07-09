from pydantic import BaseModel
from decimal import Decimal
from typing import List
from app.schemas.transaction import TransactionResponse

class Accountresponse(BaseModel):
    id: int
    account_number: str
    balance: Decimal
    
    class Config:
        from_attributes = True
        
# Extrato consolidado
class StatementResponse(BaseModel):
    account_number: str
    current_balance: Decimal
    transactions: List[TransactionResponse]