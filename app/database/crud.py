from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from app.database.models import Transaction
from app.schemas.transaction import TransactionCreate
from uuid import uuid4


async def create_transaction(db: AsyncSession, data: TransactionCreate):
    """
    Create a new transaction in the database.

    Args:
        db (AsyncSession): The database session to use for the operation.
        data (TransactionCreate): The transaction data to create.

    Returns:
        Transaction: The created transaction object.
    """
    db_tx = Transaction(**data.model_dump(), transaction_id=str(uuid4()))
    db.add(db_tx)
    await db.commit()
    await db.refresh(db_tx)
    return db_tx


async def delete_all_transactions(db: AsyncSession):
    """
    Delete all transactions from the database.

    Args:
        db (AsyncSession): The database session to use for the operation.

    Returns:
        int: The number of transactions deleted.
    """
    result = await db.execute(select(Transaction))
    transactions = result.scalars().all()

    for transaction in transactions:
        await db.delete(transaction)

    await db.commit()

    return len(transactions)
