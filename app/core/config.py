import os
from typing import List

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    # Define fields with type hints and default values.
    # pydantic-settings will automatically map these to environment variables.
    DATABASE_URL: str = "postgresql://user:password@host:port/db"
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
        # If ENV_FILE is set, it will load that file. Otherwise, it defaults to .env.
        # To disable .env loading, set ENV_FILE to a non-existent path or an empty string.
        env_file=os.getenv("ENV_FILE", ".env"),
        env_file_encoding='utf-8',
        case_sensitive=False,
        extra='ignore'
    )


settings = Settings()
