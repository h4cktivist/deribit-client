from pydantic import BaseModel, Field
from datetime import datetime
from decimal import Decimal
from typing import List


class PriceTickBase(BaseModel):
    ticker: str = Field(..., description="Currency ticker (e.g., btc_usd)")
    price: Decimal = Field(..., description="Price value")
    timestamp: datetime = Field(..., description="Timestamp of the price")


class PriceTickCreate(PriceTickBase):
    pass


class PriceTickResponse(PriceTickBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True


class PriceTickListResponse(BaseModel):
    items: List[PriceTickResponse]
    total: int


class PriceResponse(BaseModel):
    ticker: str
    price: Decimal
    timestamp: datetime
    fetched_at: datetime = Field(default_factory=datetime.utcnow)


class ErrorResponse(BaseModel):
    detail: str
