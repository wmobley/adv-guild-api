import os
from typing import List

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    # Define fields with type hints and default values.
    # pydantic-settings will automatically map these to environment variables.
    # By not providing a default value, Pydantic will raise a validation error
    # if the DATABASE_URL environment variable is not set, which is a clearer
    # error than the one you encountered.
    DATABASE_URL: str
    JWT_SECRET_KEY: str = "secret"
    JWT_ALGORITHM: str = "HS256"
    JWT_ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    API_V1_STR: str = "/api/v1"
    PROJECT_NAME: str = "Adventure Guild API"
    VERSION: str = "0.1.0"
    # pydantic-settings can parse JSON strings from env vars into lists
    BACKEND_CORS_ORIGINS: List[str] = ["http://localhost:3000", "http://localhost:8080"]
    REDIS_URL: str = "redis://localhost:6379"

    # This controls how settings are loaded.
    model_config = SettingsConfigDict(
        # By default, pydantic-settings loads from a `.env` file.
        # We are keeping this simple and predictable for development and production.
        # For tests, the environment is explicitly loaded in `tests/conftest.py`.
        env_file=".env",
        env_file_encoding='utf-8',
        case_sensitive=False,
        extra='ignore'
    )

settings = Settings()  # type: ignore [call-arg]
