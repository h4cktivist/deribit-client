from celery import Celery
import logging
from typing import Optional

from src.config import settings
from src.client.price_fetcher import PriceFetcher
from src.database import SessionLocal
from src.repository.price_repository import PriceTickCRUD

logger = logging.getLogger(__name__)

celery_app = Celery(
    "deribit_tasks",
    broker=settings.REDIS_URL,
    backend=settings.REDIS_URL,
)

celery_app.conf.update(
    task_serializer="json",
    result_serializer="json",
    accept_content=["json"],
    timezone="UTC",
    enable_utc=True,
    beat_schedule={
        "fetch-btc-price": {
            "task": "src.celery_worker.tasks.fetch_btc_price_task",
            "schedule": 60.0,
            "args": (),
        },
        "fetch-eth-price": {
            "task": "src.celery_worker.tasks.fetch_eth_price_task",
            "schedule": 60.0,
            "args": (),
        },
    }
)


@celery_app.task(bind=True, max_retries=3)
def fetch_and_store_price_task(self, currency: str) -> Optional[int]:
    logger.info(f"Starting to fetch {currency} price...")

    try:
        fetcher = PriceFetcher()
        import asyncio
        price_data = asyncio.run(fetcher.fetch_and_process_price(currency))

        if not price_data:
            logger.warning(f"No price data received for {currency}")
            return None

        db = SessionLocal()
        try:
            price_tick = PriceTickCRUD.create(db, price_data)
            db.commit()
            logger.info(f"Successfully stored {currency} price: {price_tick.price}")
            return price_tick.id
        except Exception as e:
            db.rollback()
            raise
        finally:
            db.close()

    except Exception as exc:
        logger.error(f"Error fetching {currency} price: {exc}")
        raise self.retry(exc=exc, countdown=60)


@celery_app.task
def fetch_btc_price_task() -> Optional[int]:
    logger.info("BTC task triggered by scheduler")
    return fetch_and_store_price_task("btc")


@celery_app.task
def fetch_eth_price_task() -> Optional[int]:
    logger.info("ETH task triggered by scheduler")
    return fetch_and_store_price_task("eth")


logger.info(f"Celery app configured. Beat schedule: {celery_app.conf.beat_schedule}")
