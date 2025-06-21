import pytest
from fastapi.testclient import TestClient
from typing import Generator

from app.main import app
from app.db.database import engine
from app.db.models import Base


@pytest.fixture(scope="session", autouse=True)
def db_setup_and_teardown() -> Generator[None, None, None]:
    """
    Create the database schema before the test session starts,
    and drop it after the session ends.
    """
    # The 'engine' is configured via the DATABASE_URL environment variable.
    # When running tests via Docker Compose, this is set in the 'test' service.
    # When running locally, this can be set by pytest-env via pytest.ini.
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)


@pytest.fixture(scope="module")
def api_client() -> Generator[TestClient, None, None]:
    """
    Create a TestClient instance that uses the test database.
    """
    with TestClient(app) as client:
        yield client
