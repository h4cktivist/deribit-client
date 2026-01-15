from datetime import datetime


def test_get_all_prices_success(client, mocker):
    prices = [
        mocker.Mock(
            id=1,
            ticker="btc_usd",
            price=150.0,
            timestamp=datetime.utcnow(),
            created_at=datetime.utcnow(),
        ),
        mocker.Mock(
            id=2,
            ticker="btc_usd",
            price=151.0,
            timestamp=datetime.utcnow(),
            created_at=datetime.utcnow(),
        ),
    ]

    mocker.patch(
        "src.repository.price_repository.PriceRepository.get_all_by_ticker",
        return_value=prices,
    )
    mocker.patch(
        "src.repository.price_repository.PriceRepository.get_count_by_ticker",
        return_value=2,
    )

    response = client.get("/prices")

    assert response.status_code == 200

    data = response.json()
    assert data["total"] == 2
    assert len(data["items"]) == 2


def test_get_all_prices_error(client, mocker):
    mocker.patch(
        "src.repository.price_repository.PriceRepository.get_all_by_ticker",
        side_effect=Exception("db error"),
    )

    response = client.get("/prices")

    assert response.status_code == 500
    assert "Error fetching prices" in response.json()["detail"]


def test_get_latest_price_success(client, mocker):
    price = mocker.Mock(
        ticker="btc_usd",
        price=155.0,
        timestamp=datetime.utcnow(),
    )

    mocker.patch(
        "src.repository.price_repository.PriceRepository.get_latest_price",
        return_value=price,
    )

    response = client.get("/latest")

    assert response.status_code == 200

    data = response.json()
    assert data["ticker"] == "btc_usd"
    assert float(data["price"]) == 155.0
    assert "timestamp" in data


def test_get_latest_price_not_found(client, mocker):
    mocker.patch(
        "src.repository.price_repository.PriceRepository.get_latest_price",
        return_value=None,
    )

    response = client.get("/latest")

    assert response.status_code == 404
    assert "No prices found" in response.json()["detail"]


def test_get_prices_by_date_success(client, mocker):
    prices = [
        mocker.Mock(
            id=1,
            ticker="btc_usd",
            price=150.0,
            timestamp=datetime.utcnow(),
            created_at=datetime.utcnow(),
        ),
    ]

    mocker.patch(
        "src.api.dependencies.validate_date_format",
        side_effect=[
            datetime(2024, 1, 1),
            datetime(2024, 1, 10),
        ],
    )

    mocker.patch(
        "src.repository.price_repository.PriceRepository.get_prices_by_date_range",
        return_value=prices,
    )

    response = client.get(
        "/prices-by-date",
        params={
            "start_date": "2024-01-01",
            "end_date": "2024-01-10",
        },
    )

    assert response.status_code == 200

    data = response.json()
    assert data["total"] == 1
    assert len(data["items"]) == 1


def test_get_prices_by_date_invalid_range(client, mocker):
    mocker.patch(
        "src.api.dependencies.validate_date_format",
        side_effect=[
            datetime(2024, 1, 10),
            datetime(2024, 1, 1),
        ],
    )

    response = client.get(
        "/prices-by-date",
        params={
            "start_date": "2024-01-10",
            "end_date": "2024-01-01",
        },
    )

    assert response.status_code == 400
    assert "Start date must be before end date" in response.json()["detail"]
