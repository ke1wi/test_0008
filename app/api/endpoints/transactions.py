import uuid
from typing import Annotated

from fastapi import APIRouter, Body, Depends, HTTPException
from fastapi.responses import JSONResponse
from sqlalchemy.ext.asyncio import AsyncSession

from app.celery_worker import update_statistics_wrapper, celery
from app.core.security import get_api_key
from app.database import crud, get_db
from app.core.redis import get_redis
from redis.asyncio import Redis
from app.schemas.transaction import (
    TransactionCreate,
    TransactionCreateResponse,
    TransactionDeleteResponse,
)
from pydantic import ValidationError

router = APIRouter(
    prefix="/transactions",
    tags=["transactions"],
    dependencies=[Depends(get_api_key)],
)


@router.post("/", response_model=TransactionCreateResponse)
async def create_transaction(
    transaction: Annotated[TransactionCreate, Body],
    db: AsyncSession = Depends(get_db),
):
    """
    Handle the creation of a new transaction.

    Args:
        transaction (TransactionCreate): The transaction data to be created.
        db (AsyncSession, optional): The database session. Defaults to Depends(get_db).

    Returns:
        dict: A dictionary containing a success message and a task ID.
    """
    task_id = str(uuid.uuid4())
    try:
        await crud.create_transaction(db, TransactionCreate.model_validate(transaction))
    except ValidationError:
        return JSONResponse(status_code=403, content="Validation err")

    await update_statistics_wrapper()

    return JSONResponse(
        content=TransactionCreateResponse(
            message="Transaction received", task_id=task_id
        ).model_dump(),
        status_code=202,
    )


@router.delete("/", response_model=TransactionDeleteResponse)
async def delete_all_transactions(
    db: AsyncSession = Depends(get_db), redis: Redis = Depends(get_redis)
):
    """
    Handle the deletion of a transaction.

    Args:
        transaction_id (str): The ID of the transaction to be deleted.
        db (AsyncSession, optional): The database session. Defaults to Depends(get_db).

    Returns:
        dict: A dictionary containing a success message.
    """
    amount = await crud.delete_all_transactions(db)
    await redis.delete("statistics")
    return TransactionDeleteResponse(message="Transactions deleted", amount=amount)
