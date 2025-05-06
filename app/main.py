from fastapi import FastAPI

from app.api.endpoints import health, statistics, transactions

app = FastAPI(
    title="Transaction Service API",
    description="API для роботи з транзакціями та статистикою",
    version="1.0.0",
)


app.include_router(transactions.router)
app.include_router(statistics.router)
app.include_router(health.router)
