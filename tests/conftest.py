from unittest.mock import MagicMock

import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient

from src.api.router import router
from src.database import get_db
from src.api.dependencies import validate_ticker


@pytest.fixture
def mock_db():
    return MagicMock()


@pytest.fixture
def app(mock_db):
    app = FastAPI()
    app.include_router(router)

    app.dependency_overrides[get_db] = lambda: mock_db
    app.dependency_overrides[validate_ticker] = lambda: "AAPL"

    yield app

    app.dependency_overrides.clear()


@pytest.fixture
def client(app):
    return TestClient(app)
