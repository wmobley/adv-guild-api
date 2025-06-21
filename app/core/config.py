import os
from typing import List

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    DATABASE_URL: str = os.getenv("DATABASE_URL", "postgresql://user:password@host:port/db")
    JWT_SECRET_KEY: str = os.getenv("JWT_SECRET_KEY", "secret")
    JWT_ALGORITHM: str = os.getenv("JWT_ALGORITHM", "HS256")
    JWT_ACCESS_TOKEN_EXPIRE_MINUTES: int = int(os.getenv("JWT_ACCESS_TOKEN_EXPIRE_MINUTES", 30))
    API_V1_STR: str = "/api/v1"
    PROJECT_NAME: str = "Adventure Guild API"
    VERSION: str = os.getenv("VERSION", "0.1.0")
    BACKEND_CORS_ORIGINS: List[str] = ["http://localhost:3000", "http://localhost:8080"]


settings = Settings()