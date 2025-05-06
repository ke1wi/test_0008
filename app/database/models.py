from sqlalchemy import Column, DateTime, Float, String

from app.database.base import Base
from uuid import uuid4


class Transaction(Base):
    __tablename__ = "transactions"

    transaction_id = Column(String, primary_key=True, index=True)
    user_id = Column(String, index=True)
    amount = Column(Float)
    currency = Column(String)
    timestamp = Column(DateTime)
