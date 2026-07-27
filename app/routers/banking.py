from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.core.security import get_current_user
from app.models.account import User
from app.schemas. transaction import TransactionCreate, TransactionResponse
from app.schemas.account import StatementResponse
from app.services.bank_service import BankService

router = APIRouter(prefix="/banking", tags=["Banking Operations"])

@router.post("/transaction", response_model=TransactionResponse)
async def create_transaction(
    transaction_data: TransactionCreate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    # Toda a regra de negocio transferida para o service
    return await BankService.create_transaction(
        db=db,
        user_id=current_user.id,
        transaction_data=transaction_data
    )

@router.get("/statement", response_model=StatementResponse)
async def get_statement(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    # Toda a regra de negocio transferida para o service
    return await BankService.get_statement(
        db=db,
        user_id=current_user.id
    )