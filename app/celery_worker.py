import heapq
import json

from aio_celery import Celery  # type: ignore
from loguru import logger
from sqlalchemy.future import select

from app.core.redis import get_redis
from app.core.config import config
from app.database import get_db
from app.database.models import Transaction
from app.schemas.statistics import Statistics

celery = Celery("statistics_worker")
celery.conf.update(result_backend=config.REDIS_URL, broker_url=config.RABBITMQ_URL)

logger.add(
    "logs/statistics_worker.log", level="INFO", rotation="1 MB", compression="zip"
)


async def update_statistics_wrapper():
    async with celery.setup():
        await update_statistics()


@celery.task(name="update_statistics")
async def update_statistics():
    logger.info("Updating statistics...")

    async for session in get_db():
        total_sum = 0.0
        count = 0
        min_heap = []
        top_n = 3

        result = await session.stream_scalars(select(Transaction))
        async for tx in result:
            total_sum += tx.amount
            count += 1

            if len(min_heap) < top_n:
                heapq.heappush(min_heap, (tx.amount, tx.transaction_id))
            else:
                heapq.heappushpop(min_heap, (tx.amount, tx.transaction_id))

        average = total_sum / count if count else 0.0
        top_transactions = sorted(min_heap, reverse=True)

        statistics = Statistics(
            total_transactions=count,
            average_transaction_amount=average,
            top_transactions=[
                {"transaction_id": tx_id, "amount": amount}
                for amount, tx_id in top_transactions
            ],
        )

        async for redis in get_redis():
            await redis.set(
                "statistics", json.dumps(statistics.model_dump(mode="json"))
            )

        logger.success("Statistics updated and cached successfully.")
