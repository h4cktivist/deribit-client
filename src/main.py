from fastapi import FastAPI
from contextlib import asynccontextmanager
import logging
import uvicorn

from src.config import settings
from src.database import init_db
from src.api.router import router as api_router

logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Starting application...")
    init_db()
    logger.info("Database initialized")

    yield

    logger.info("Shutting down application...")


app = FastAPI(
    title="Deribit Price API",
    description="API for fetching and retrieving cryptocurrency prices from Deribit",
    version="1.0.0",
    lifespan=lifespan
)

app.include_router(
    api_router,
    prefix=settings.API_V1_PREFIX,
    tags=["prices"]
)

@app.get("/")
async def root():
    return {
        "message": "Deribit Price API",
        "docs": "/docs",
    }


if __name__ == "__main__":
    uvicorn.run(
        "src.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True
    )
