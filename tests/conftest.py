import os
import pytest
from typing import Dict, Any, Generator
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.pool import StaticPool

# Set required environment variables for testing before importing app modules
os.environ.setdefault("DATABASE_URL", "sqlite:///:memory:")
os.environ.setdefault("JWT_SECRET_KEY", "test-secret-key-for-testing-only")

from app.main import app
from app.db.database import get_db
from app.db.models import Base
from app.db import models

# Use in-memory SQLite for testing
SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def override_get_db() -> Generator[Session, None, None]:
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()


@pytest.fixture(scope="function")
def client() -> Generator[TestClient, None, None]:
    # Override the dependency
    app.dependency_overrides[get_db] = override_get_db
    
    # Create tables
    Base.metadata.create_all(bind=engine)
    
    # Create test client
    with TestClient(app) as test_client:
        yield test_client
    
    # Clean up
    Base.metadata.drop_all(bind=engine)
    app.dependency_overrides.clear()


@pytest.fixture(scope="function")
def db() -> Generator[Session, None, None]:
    Base.metadata.create_all(bind=engine)
    db_session = TestingSessionLocal()
    try:
        yield db_session
    finally:
        db_session.close()
        Base.metadata.drop_all(bind=engine)


@pytest.fixture
def sample_reference_data(db: Session) -> Dict[str, Any]:
    """Create sample reference data for tests."""
    quest_type = models.QuestType(name="Adventure")
    difficulty = models.Difficulty(name="Medium")
    interest = models.Interest(name="Exploration")
    location = models.Location(
        name="Test Location",
        latitude=40.7128,
        longitude=-74.0060,
        description="A test location for quests"
    )
    
    db.add_all([quest_type, difficulty, interest, location])
    db.commit()
    
    return {
        'quest_type': quest_type,
        'difficulty': difficulty,
        'interest': interest,
        'location': location
    }