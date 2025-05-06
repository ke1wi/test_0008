from typing import List, Optional

from pydantic import BaseModel, Field


class TopTransaction(BaseModel):
    transaction_id: str = Field(
        ..., description="Unique identifier for the transaction"
    )
    amount: float = Field(..., description="Amount of the transaction")


class Statistics(BaseModel):
    total_transactions: int = Field(..., description="Total number of transactions")
    average_transaction_amount: Optional[float] = Field(
        None, description="Average amount of transactions"
    )
    top_transactions: Optional[List[TopTransaction]] = Field(
        None, description="List of top transactions"
    )
