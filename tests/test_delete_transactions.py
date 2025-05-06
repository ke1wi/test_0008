import pytest
from httpx import AsyncClient

from app.core.config import config


@pytest.mark.asyncio
async def test_delete_all_transactions(client: AsyncClient):
    response = await client.delete(
        "/transactions/", headers={"Authorization": f"ApiKey {config.API_KEY}"}
    )
    assert response.status_code == 200
    assert "amount" in response.json()
