import pytest
from fastapi.testclient import TestClient
from app.main import app
from typing import Generator


@pytest.fixture(scope="module")
def client() -> Generator[TestClient, None, None]:
    """
    Create a TestClient instance that can be used in tests.
    """
    test_client = TestClient(app)
    yield test_client
    test_client.close()
