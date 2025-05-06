import asyncio
from typing import Any, AsyncGenerator

import pytest_asyncio
from httpx import ASGITransport, AsyncClient
from redis.asyncio import Redis
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from app.core.redis import get_redis
from app.database import get_db
from app.database.models import Base
from app.main import app

TEST_DB_URL = "sqlite+aiosqlite:///./tests/test.db"

engine_test = create_async_engine(TEST_DB_URL, future=True, echo=False)
TestingAsyncSessionLocal = async_sessionmaker(
    bind=engine_test, class_=AsyncSession, expire_on_commit=False
)
redis_client = Redis(host="127.0.0.1", port=6379, db=0, decode_responses=True)


@pytest_asyncio.fixture(scope="session")
def event_loop():
    """Create an instance of the default event loop for each test session."""

    policy = asyncio.get_event_loop_policy()
    loop = policy.new_event_loop()
    yield loop
    loop.close()


async def override_get_db() -> AsyncGenerator[AsyncSession, None]:
    async with TestingAsyncSessionLocal() as session:
        yield session


async def override_get_redis() -> AsyncGenerator[AsyncSession, None]:
    yield redis_client


app.dependency_overrides[get_db] = override_get_db
app.dependency_overrides[get_redis] = override_get_redis


@pytest_asyncio.fixture(scope="session", autouse=True)
async def create_test_db():
    async with engine_test.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)


@pytest_asyncio.fixture
async def client() -> AsyncGenerator[AsyncClient, None]:
    async with AsyncClient(
        transport=ASGITransport(app), base_url="http://test", follow_redirects=True
    ) as ac:
        yield ac


@pytest_asyncio.fixture(scope="session")
async def redis() -> AsyncGenerator[Redis, Any]:
    """Fixture for Redis client to be used across tests."""
    redis = Redis.from_url(
        "redis://localhost:6379/0",
        decode_responses=True,
        socket_connect_timeout=1,
        socket_timeout=1,
    )
    try:
        await redis.ping()
        yield redis
    finally:
        await redis.aclose()
