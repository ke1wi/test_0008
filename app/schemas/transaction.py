from datetime import UTC, datetime

from pydantic import BaseModel, Field
from uuid import UUID
from typing import Union


class TransactionCreate(BaseModel):
    user_id: str = Field(..., description="User ID", examples=["user_001"])
    amount: float = Field(..., description="Transaction amount", examples=[150.50])
    currency: str = Field(..., description="Transaction currency", examples=["USD"])
    timestamp: datetime = Field(
        default_factory=lambda: datetime.now(UTC),
        description="Transaction timestamp",
        examples=["2024-12-12T12:00:00"],
    )


class Transaction(TransactionCreate):
    transaction_id: Union[UUID, str] = Field(
        ..., description="Transaction ID", examples=["123456"]
    )


class TransactionCreateResponse(BaseModel):
    message: str = Field(
        ..., description="Response message", examples=["Transaction received"]
    )
    task_id: str = Field(..., description="Task ID", examples=["abcd1234"])


class TransactionDeleteResponse(BaseModel):
    message: str = Field(
        ..., description="Response message", examples=["Transactions deleted"]
    )
    amount: int = Field(..., description="Number of deleted transactions", examples=[5])
