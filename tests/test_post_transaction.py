import uuid

import pytest
from httpx import AsyncClient

from app.core.config import config
from app.schemas.transaction import TransactionCreate


@pytest.mark.asyncio
async def test_create_transaction(client: AsyncClient):
    transaction = TransactionCreate(
        transaction_id=str(uuid.uuid4()),
        user_id="test_user",
        amount=100.50,
        currency="USD",
    )

    transaction_dict = transaction.model_dump()
    transaction_dict["timestamp"] = transaction.timestamp

    response = await client.post(
        "/transactions/",
        json=transaction.model_dump(mode="json"),
        headers={"Authorization": f"ApiKey {config.API_KEY}"},
    )

    assert response.status_code == 202
    assert "task_id" in response.json()
