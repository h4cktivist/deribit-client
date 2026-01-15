# Deribit Price API

API для получения и хранения цен криптовалют с биржи Deribit.


## Функциональность

- Каждую минуту получает цены BTC/USD и ETH/USD с Deribit API
- Сохраняет данные в PostgreSQL
- Предоставляет REST API для доступа к данным


## API Endpoints

### GET /api/v1/prices
Получить все сохраненные данные по указанной валюте

**Параметры:**
- `ticker` (обязательный) - тикер валюты (btc_usd или eth_usd)
- `skip` - пропустить первые N записей (по умолчанию 0)
- `limit` - количество записей (по умолчанию 100, максимум 1000)

### GET /api/v1/latest
Получить последнюю цену валюты

**Параметры:**
- `ticker` (обязательный) - тикер валюты

### GET /api/v1/prices-by-date
Получить цены валюты с фильтром по дате

**Параметры:**
- `ticker` (обязательный) - тикер валюты
- `start_date` - начальная дата (YYYY-MM-DD или YYYY-MM-DD HH:MM:SS)
- `end_date` - конечная дата (YYYY-MM-DD или YYYY-MM-DD HH:MM:SS)


## Установка и запуск

```bash
# Создать .env файл
cp .env.example .env

# Запустить приложение
docker-compose up --build -d
```

Приложение будет доступно по адресу: http://localhost:8000

Swagger-документация доступна по адресу: http://localhost:8000/docs


## Design decisions

- Разделение на слои: API и репозиторий работы с базой данных
- Использование dependency injection
- Использование aiohttp для HTTP-запросов к Deribit API
- Использование SQLAlchemy ORM для абстракции базы данных
- Использование Celery для фоновых задач
- Многоконтейнерная архитектура: приложение, БД, Redis и Celery (+ flower)
