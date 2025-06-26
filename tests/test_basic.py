"""Basic tests to verify test setup is working"""

from fastapi.testclient import TestClient


def test_basic_math() -> None:
    """Basic test to verify pytest is working"""
    assert 1 + 1 == 2


def test_import_app() -> None:
    """Test that we can import the FastAPI app"""
    from app.main import app
    assert app is not None


def test_client_creation(client: TestClient) -> None:
    """Test that test client can be created"""
    assert client is not None