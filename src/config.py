from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    DATABASE_URL: str

    REDIS_URL: str = "redis://localhost:6379/0"

    DERIBIT_BASE_URL: str = "https://test.deribit.com/api/v2"
    API_V1_PREFIX: str = "/api/v1"

    class Config:
        env_file = ".env"
        case_sensitive = True


settings = Settings()
