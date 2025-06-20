import pytest
from datetime import datetime
from unittest.mock import patch, Mock # Import Mock for type hinting
from fastapi.testclient import TestClient
from typing import List, Dict, Any # For type hinting
from app.main import app
from app.db import schemas
from types import SimpleNamespace
client = TestClient(app) # Correct: app is a positional argument

def test_get_campaigns_success(client: TestClient) -> None: # Added client parameter and return type
    # Create real campaign data instead of mocks
    mock_campaigns = [
        {
            "id": 1,
            "title": "Test Campaign 1",
            "description": "Test Description 1",
            "author_id": 1,
            "created_at": datetime.now(),
            "updated_at": datetime.now()
        },
        {
            "id": 2,
            "title": "Test Campaign 2", 
            "description": "Test Description 2",
            "author_id": 1,
            "created_at": datetime.now(),
            "updated_at": datetime.now()
        }
    ]
    
    # Mock the CRUD function to return real data
    with patch("app.db.crud_campaigns.get_campaigns") as mock_crud_get_campaigns: # Renamed for clarity
        # Use SimpleNamespace to create object-like instances
        campaign1 = SimpleNamespace(
            id=1,
            title='Test Campaign 1',
            description='Test Description 1',
            author_id=1,
            is_public=True,
            created_at=datetime.now(),
            updated_at=datetime.now()
        )
        
        campaign2 = SimpleNamespace(
            id=2,
            title='Test Campaign 2',
            description='Test Description 2',
            author_id=1,
            is_public=True,
            created_at=datetime.now(),
            updated_at=datetime.now()
        )
        
        mock_crud_get_campaigns.return_value = [campaign1, campaign2]
        
        response = client.get("/api/v1/campaigns/")
        
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 2
        assert data[0]["title"] == "Test Campaign 1"
