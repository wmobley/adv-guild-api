import pytest
from datetime import datetime
from unittest.mock import patch, Mock # Import Mock
from fastapi.testclient import TestClient
from sqlalchemy.exc import SQLAlchemyError # Add this import
from typing import List, Any # For type hints
from app.main import app
from types import SimpleNamespace

client = TestClient(app) # Correct: app is a positional argument

def test_get_interests_success(client: TestClient) -> None:
    with patch("app.db.crud.get_interests") as mock_get_interests:
        interest1 = SimpleNamespace(
            id=1,
            name='Test Interest 1',
            description='Test Description 1',
            created_at=datetime.now(),
            updated_at=datetime.now()
        )
        
        interest2 = SimpleNamespace(
            id=2,
            name='Test Interest 2',
            description='Test Description 2',
            created_at=datetime.now(),
            updated_at=datetime.now()
        )
        
        mock_get_interests.return_value = [interest1, interest2]
        
        response = client.get("/api/v1/reference/interests")
        
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 2
        assert data[0]["name"] == "Test Interest 1"
        assert data[1]["name"] == "Test Interest 2"

def test_get_interests_empty(client: TestClient) -> None:
    with patch("app.db.crud.get_interests") as mock_get_interests:
        mock_get_interests.return_value = []
        
        response = client.get("/api/v1/reference/interests")
        
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 0

@patch('app.db.crud.get_interests')
def test_get_interests_db_error(mock_get_interests: Mock, client: TestClient) -> None: # Changed type hint to Mock
    mock_get_interests.side_effect = SQLAlchemyError("Database connection failed")
    
    response = client.get("/api/v1/reference/interests")
    
    # Expect 500 error when database fails
    assert response.status_code == 500
    data = response.json()
    assert "detail" in data
