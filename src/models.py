from sqlalchemy import Column, Integer, String, DateTime, Numeric, Index
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

Base = declarative_base()


class PriceTick(Base):
    __tablename__ = "price_ticks"

    id = Column(Integer, primary_key=True, index=True)
    ticker = Column(String(10), nullable=False, index=True)
    price = Column(Numeric(20, 8), nullable=False)
    timestamp = Column(DateTime, nullable=False, index=True)
    created_at = Column(DateTime, default=datetime.now)

    __table_args__ = (
        Index("idx_ticker_timestamp", "ticker", "timestamp"),
    )

    def __repr__(self) -> str:
        return f"<PriceTick(ticker={self.ticker}, price={self.price}, timestamp={self.timestamp})>"
