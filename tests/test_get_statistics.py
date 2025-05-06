import pytest
import json
from httpx import AsyncClient
from redis.asyncio import Redis

from app.core.config import config
from app.schemas.statistics import Statistics, TopTransaction


@pytest.mark.asyncio
async def test_get_statistics(redis: Redis, client: AsyncClient):
    """
    Test the `/statistics` endpoint to ensure it returns the correct data.

    This test performs the following checks:
    - Verifies that the endpoint responds with a 200 status code.
    - Confirms the presence of the `average_transaction_amount` and `top_transactions` keys in the response JSON.
    - Ensures that `top_transactions` is a list and contains at most 3 items.
    """

    test_statistics = Statistics(
        total_transactions=3,
        average_transaction_amount=150.75,
        top_transactions=[
            TopTransaction(transaction_id=i, amount=i * 50) for i in range(1, 4)
        ],
    )
    await redis.set("statistics", json.dumps(test_statistics.model_dump(mode="json")))

    response = await client.get(
        "/statistics/", headers={"Authorization": f"ApiKey {config.API_KEY}"}
    )

    assert response.status_code == 200, f"Expected 200, got {response.status_code}"

    data = response.json()

    assert "total_transactions" in data, "Missing 'total_transactions' in response"
    if data["total_transactions"]:
        assert (
            "average_transaction_amount" in data
        ), "Missing 'average_transaction_amount' in response"
        assert "top_transactions" in data, "Missing 'top_transactions' in response"
        assert isinstance(
            data["top_transactions"], list
        ), "'top_transactions' is not a list"
        assert (
            len(data["top_transactions"]) <= 3
        ), "'top_transactions' contains more than 3 items"

    else:
        assert (
            data["average_transaction_amount"] == 0.0
        ), "Expected average 0.0 when no transactions"
        assert (
            data["top_transactions"] == []
        ), "Expected empty top_transactions when no transactions"
