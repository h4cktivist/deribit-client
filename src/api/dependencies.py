from fastapi import HTTPException, Query
from datetime import datetime


def validate_ticker(ticker: str = Query(..., description="Currency ticker (e.g., btc_usd)")) -> str:
    if ticker.lower() not in ["btc_usd", "eth_usd"]:
        raise HTTPException(
            status_code=400,
            detail="Invalid ticker. Supported values: btc_usd, eth_usd"
        )
    return ticker.lower()


def validate_date_format(date_str: str) -> datetime:
    try:
        for fmt in ("%Y-%m-%d", "%Y-%m-%d %H:%M:%S", "%Y-%m-%dT%H:%M:%S"):
            try:
                return datetime.strptime(date_str, fmt)
            except ValueError:
                continue
        raise ValueError
    except ValueError:
        raise HTTPException(
            status_code=400,
            detail="Invalid date format. Use YYYY-MM-DD or YYYY-MM-DD HH:MM:SS"
        )
