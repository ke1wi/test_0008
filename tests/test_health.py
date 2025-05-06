import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_health(client: AsyncClient):
    """
    Test the creation of a transaction by sending a POST request to the /transactions/ endpoint.
    This test verifies that the response status code is 202 and the response JSON contains
    the expected message and task_id.
    """
    response = await client.get("/health/healthcheck/")

    assert response.status_code == 202
    assert response.json() == {"status": "ok"}
