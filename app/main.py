from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from typing import Dict, Any, AsyncGenerator

from app.core.config import settings
from app.db.database import engine
from app.db.models import Base
from app.api.v1.api import api_router
import os
import json


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    # Create tables on startup
    Base.metadata.create_all(bind=engine)
    yield


app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    description="Adventure Guild API - Manage quests, campaigns, and guild members",
    openapi_url=f"{settings.API_V1_STR}/openapi.json",
    docs_url="/docs",
    redoc_url="/redoc",
    lifespan=lifespan
)

BACKEND_CORS_ORIGINS_STR = os.getenv("BACKEND_CORS_ORIGINS")
allowed_origins = []

if BACKEND_CORS_ORIGINS_STR:
    try:
        # Assuming the env var is a JSON string array e.g., '["http://localhost:3000"]'
        allowed_origins = json.loads(BACKEND_CORS_ORIGINS_STR)
    except json.JSONDecodeError:
        # Fallback for comma-separated list e.g., "http://localhost:3000,http://localhost:8081"
        allowed_origins = [origin.strip() for origin in BACKEND_CORS_ORIGINS_STR.split(',')]

# Set up CORS
if settings.BACKEND_CORS_ORIGINS:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=[str(origin) for origin in settings.BACKEND_CORS_ORIGINS],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

app.include_router(api_router, prefix=settings.API_V1_STR)


@app.get("/")
async def root() -> Dict[str, Any]:
    return {
        "message": "Adventure Guild API",
        "version": settings.VERSION,
        "docs": "/docs"
    }


@app.get("/health")
async def health_check() -> Dict[str, str]:
    return {"status": "healthy"}