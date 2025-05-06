from fastapi import APIRouter, Depends
from redis.asyncio import Redis

from app.core.redis import get_redis
from app.core.security import get_api_key
from app.schemas.statistics import Statistics

router = APIRouter(
    prefix="/statistics",
    tags=["statistics"],
    dependencies=[Depends(get_api_key)],
)


@router.get("/", response_model=Statistics)
async def calculate_statistics(redis: Redis = Depends(get_redis)) -> Statistics:
    """
    Get pre-calculated statistics from Redis cache.

    Returns:
        Statistics: Cached transaction statistics.
    """
    cached = await redis.get("statistics")
    if not cached:
        return Statistics(total_transactions=0).model_dump(mode="json")
    return Statistics.model_validate_json(cached)
