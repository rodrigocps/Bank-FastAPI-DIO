from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload

from app.core.database import get_db
from app.core.security import get_current_user
from app.models.account import User, Account
from app.models.transaction import Transaction, TransactionType
from app.schemas. transaction import TransactionCreate, TransactionResponse
from app.schemas.account import StatementResponse

# doas as rotas deste router exigirão que o usuario esteja logado
router = APIRouter(prefix="/banking", tags=["Banking Operations"])

@router.post("/transaction", response_model=TransactionResponse)
async def create_transaction(
    transaction_data: TransactionCreate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    # 1. Busca a conta vinculada ao usuário logado
    result = await db.execute(select(Account).where(Account.user_id == current_user.id))
    account = result.scalars().first()
    
    if not account:
        raise HTTPException(status_code=404, detail="Account not found.")
    
    # 2. Lógica de Saque
    if transaction_data.type == TransactionType.WITHDRAWAL:
        # Verifica instantaneamente se osaldo é maior ou igual ao valor do saque
        if account.balance < transaction_data.amount:
            raise HTTPException(status_code=400, detail="Insufficient balance to make the withdrawal.")
        account.balance -= transaction_data.amount
        
    # 3. Lógica de Deposito
    elif transaction_data.type == TransactionType.DEPOSIT:
        account.balance += transaction_data.amount
        
    # 4. Grava a movimentação do "livro-razão" (imutavel)
    new_transaction = Transaction(
        account_id=account.id,
        type=transaction_data.type,
        amount=transaction_data.amount
    )
    
    db.add(new_transaction)
    # Atualiza a conta e grava a transação ao mesmo tempo para garantir integridade
    await db.commit()
    await db.refresh(new_transaction)
    
    return new_transaction

@router.get("/statement", response_model=StatementResponse)
async def get_statement(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    # busca a conta ja trazendo as transações relacionadas usando 'selectinload'
    # Essa abordagem evita o problema de "lazy loading" em contextos assincronos
    query = select(Account).options(selectinload(Account.transactions)).where(Account.user_id == current_user.id)
    result = await db.execute(query)
    account = result.scalars().first()
    
    if not account:
        raise HTTPException(status_code=404, detail="Account not found.")

    # Retorna o extrato consolidando os dados da conta e todas as transações (filtradas pelo account_id internamente) 
    return {
        "account_number": account.account_number,
        "current_balance": account.balance,
        "transactions": account.transactions
    }