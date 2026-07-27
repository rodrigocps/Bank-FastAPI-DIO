from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload

from app.models.account import Account
from app.models.transaction import Transaction, TransactionType
from app.schemas. transaction import TransactionCreate


class BankService:
    @staticmethod
    async def create_transaction(
        db: AsyncSession,
        user_id: int,
        transaction_data: TransactionCreate
    ) -> Transaction:
        # Busca a conta vinculada ao usuário logado
        result = await db.execute(select(Account).where(Account.user_id == user_id))
        account = result.scalars().first()
        
        if not account:
            raise HTTPException(status_code=404, detail="Account not found.")
        
        # Lógica de Saque
        if transaction_data.type == TransactionType.WITHDRAWAL:
            # Verifica instantaneamente se o saldo é maior ou igual ao valor do saque
            if account.balance < transaction_data.amount:
                raise HTTPException(status_code=400, detail="Insufficient balance to make the withdrawal.")
            account.balance -= transaction_data.amount
            
        # Lógica de Deposito
        elif transaction_data.type == TransactionType.DEPOSIT:
            account.balance += transaction_data.amount
            
        # Grava a movimentação do "livro-razão" (imutavel)
        new_transaction = Transaction(
            account_id=account.id,
            type=transaction_data.type,
            amount=transaction_data.amount
        )
        
        db.add(new_transaction)
        await db.commit()
        await db.refresh(new_transaction)
        
        return new_transaction

    @staticmethod
    async def get_statement(
        db: AsyncSession,
        user_id: int        
    ) -> dict:
        query = (select(Account).options(selectinload(Account.transactions)).where(Account.user_id == user_id))
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