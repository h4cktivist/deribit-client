import aiohttp
import asyncio
from typing import Dict, Any, Optional
import logging

from src.config import settings

logger = logging.getLogger(__name__)


class DeribitClient:
    def __init__(self, base_url: str = None):
        self.base_url = base_url or settings.DERIBIT_BASE_URL
        self.session: Optional[aiohttp.ClientSession] = None

    async def __aenter__(self):
        await self.connect()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.disconnect()

    async def connect(self) -> None:
        if not self.session or self.session.closed:
            timeout = aiohttp.ClientTimeout(total=30)
            self.session = aiohttp.ClientSession(timeout=timeout)
            logger.info("Deribit client connected")

    async def disconnect(self) -> None:
        if self.session and not self.session.closed:
            await self.session.close()
            logger.info("Deribit client disconnected")

    async def get_index_price(self, currency: str) -> Optional[Dict[str, Any]]:
        if not self.session:
            await self.connect()

        try:
            async with self.session.get(
                    f"{self.base_url}/public/get_index_price",
                    params={"index_name": currency}
            ) as response:
                if response.status == 200:
                    data = await response.json()
                    return data.get("result")
                else:
                    logger.error(f"Error fetching price for {currency}: {response.status}")
                    return None

        except aiohttp.ClientError as e:
            logger.error(f"Client error fetching price for {currency}: {e}")
            return None
        except asyncio.TimeoutError:
            logger.error(f"Timeout fetching price for {currency}")
            return None

    async def fetch_btc_price(self) -> Optional[Dict[str, Any]]:
        return await self.get_index_price("btc_usd")

    async def fetch_eth_price(self) -> Optional[Dict[str, Any]]:
        return await self.get_index_price("eth_usd")
