from typing import Dict, Any, Optional
from decimal import Decimal
from datetime import datetime
import logging

from src.client.deribit_client import DeribitClient
from src.schemas import PriceTickCreate

logger = logging.getLogger(__name__)


class PriceFetcher:
    def __init__(self):
        self.client = DeribitClient()

    async def fetch_and_process_price(self, currency: str) -> Optional[PriceTickCreate]:
        try:
            async with self.client as client:
                if currency.lower() == "btc":
                    data = await client.fetch_btc_price()
                elif currency.lower() == "eth":
                    data = await client.fetch_eth_price()
                else:
                    logger.error(f"Unsupported currency: {currency}")
                    return None

                if data:
                    return self._parse_price_data(data, currency)
                return None

        except Exception as e:
            logger.error(f"Error fetching {currency} price: {e}")
            return None

    def _parse_price_data(
            self,
            data: Dict[str, Any],
            currency: str
    ) -> PriceTickCreate:
        ticker = f"{currency.lower()}_usd"
        price = Decimal(str(data.get("index_price", 0)))

        timestamp_ms = data.get("timestamp", 0)
        timestamp = datetime.fromtimestamp(timestamp_ms / 1000)

        return PriceTickCreate(
            ticker=ticker,
            price=price,
            timestamp=timestamp
        )
