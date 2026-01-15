from sqlalchemy.orm import Session
from sqlalchemy import desc, and_
from datetime import datetime
from typing import Optional
import logging

from src.models import PriceTick
from src.schemas import PriceTickCreate

logger = logging.getLogger(__name__)


class PriceRepository:
    @staticmethod
    def create(db: Session, price_tick: PriceTickCreate) -> PriceTick:
        db_price_tick = PriceTick(
            ticker=price_tick.ticker,
            price=price_tick.price,
            timestamp=price_tick.timestamp
        )
        db.add(db_price_tick)
        db.flush()
        logger.debug(f"Created price tick: {db_price_tick}")
        return db_price_tick

    @staticmethod
    def get_all_by_ticker(
            db: Session,
            ticker: str,
            skip: int = 0,
            limit: int = 100
    ) -> list[type[PriceTick]]:
        return db.query(PriceTick) \
            .filter(PriceTick.ticker == ticker) \
            .order_by(desc(PriceTick.timestamp)) \
            .offset(skip) \
            .limit(limit) \
            .all()

    @staticmethod
    def get_latest_price(db: Session, ticker: str) -> Optional[PriceTick]:
        return db.query(PriceTick) \
            .filter(PriceTick.ticker == ticker) \
            .order_by(desc(PriceTick.timestamp)) \
            .first()

    @staticmethod
    def get_prices_by_date_range(
            db: Session,
            ticker: str,
            start_date: datetime,
            end_date: datetime,
            skip: int = 0,
            limit: int = 100
    ) -> list[type[PriceTick]]:
        return db.query(PriceTick) \
            .filter(
            and_(
                PriceTick.ticker == ticker,
                PriceTick.timestamp >= start_date,
                PriceTick.timestamp <= end_date
            )
        ) \
            .order_by(desc(PriceTick.timestamp)) \
            .offset(skip) \
            .limit(limit) \
            .all()

    @staticmethod
    def get_count_by_ticker(db: Session, ticker: str) -> int:
        return db.query(PriceTick) \
            .filter(PriceTick.ticker == ticker) \
            .count()
