from fastapi import APIRouter, Depends, Query, HTTPException
from sqlalchemy.orm import Session
from datetime import timedelta

from src.database import get_db
from src.schemas import (
    PriceTickListResponse,
    PriceResponse,
    ErrorResponse
)
from src.repository.price_repository import PriceTickCRUD
from src.api.dependencies import validate_ticker, validate_date_format

router = APIRouter()


@router.get(
    "/prices",
    response_model=PriceTickListResponse,
    responses={400: {"model": ErrorResponse}}
)
def get_all_prices(
    ticker: str = Depends(validate_ticker),
    skip: int = Query(0, ge=0, description="Number of records to skip"),
    limit: int = Query(100, ge=1, le=1000, description="Number of records to return"),
    db: Session = Depends(get_db)
) -> PriceTickListResponse:
    try:
        prices = PriceTickCRUD.get_all_by_ticker(db, ticker, skip, limit)
        total = PriceTickCRUD.get_count_by_ticker(db, ticker)

        return PriceTickListResponse(
            items=prices,
            total=total
        )
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error fetching prices: {str(e)}"
        )


@router.get(
    "/latest",
    response_model=PriceResponse,
    responses={
        404: {"model": ErrorResponse},
        400: {"model": ErrorResponse}
    }
)
def get_latest_price(
    ticker: str = Depends(validate_ticker),
    db: Session = Depends(get_db)
) -> PriceResponse:
    try:
        price_tick = PriceTickCRUD.get_latest_price(db, ticker)

        if not price_tick:
            raise HTTPException(
                status_code=404,
                detail=f"No prices found for ticker: {ticker}"
            )

        return PriceResponse(
            ticker=price_tick.ticker,
            price=price_tick.price,
            timestamp=price_tick.timestamp
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error fetching latest price: {str(e)}"
        )


@router.get(
    "/prices-by-date",
    response_model=PriceTickListResponse,
    responses={400: {"model": ErrorResponse}}
)
def get_prices_by_date(
    ticker: str = Depends(validate_ticker),
    start_date: str = Query(..., description="Start date (YYYY-MM-DD or YYYY-MM-DD HH:MM:SS)"),
    end_date: str = Query(..., description="End date (YYYY-MM-DD or YYYY-MM-DD HH:MM:SS)"),
    skip: int = Query(0, ge=0, description="Number of records to skip"),
    limit: int = Query(100, ge=1, le=1000, description="Number of records to return"),
    db: Session = Depends(get_db)
) -> PriceTickListResponse:
    try:
        start = validate_date_format(start_date)
        end = validate_date_format(end_date)

        if start > end:
            raise HTTPException(
                status_code=400,
                detail="Start date must be before end date"
            )

        end = end + timedelta(days=1)

        prices = PriceTickCRUD.get_prices_by_date_range(
            db, ticker, start, end, skip, limit
        )

        total = len(prices)
        return PriceTickListResponse(
            items=prices,
            total=total
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error fetching prices by date: {str(e)}"
        )
