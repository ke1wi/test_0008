from redis.asyncio import Redis

from app.core.config import config


async def get_redis():
    redis = Redis.from_url(config.REDIS_URL, decode_responses=True)
    yield redis
