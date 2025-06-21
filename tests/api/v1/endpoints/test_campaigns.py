import pytest
from datetime import datetime
from unittest.mock import patch, Mock # Import Mock for type hinting
from fastapi.testclient import TestClient
from typing import List, Dict, Any # For type hinting
from app.main import app
from app.db import schemas
from types import SimpleNamespace

def create_mock_campaign_data(campaign_id: int, title: str) -> Dict[str, Any]:
    """Helper function to create mock campaign data."""
    return {
        "id": campaign_id,
        "title": title,
        "description": f"Description for {title}",
        "author_id": 1,
        "is_public": True,
        "created_at": datetime.now(),
        "updated_at": datetime.now(),
    }


def test_get_campaigns_success(api_client: TestClient) -> None:
    # Mock the CRUD function to return real data
    with patch("app.db.crud_campaigns.get_campaigns") as mock_crud_get_campaigns:
        # Create mock ORM-like objects
        mock_campaign_orm_1 = SimpleNamespace(**create_mock_campaign_data(1, "Test Campaign 1"))
        mock_campaign_orm_2 = SimpleNamespace(**create_mock_campaign_data(2, "Test Campaign 2"))

        mock_crud_get_campaigns.return_value = [mock_campaign_orm_1, mock_campaign_orm_2]

        response = api_client.get("/api/v1/campaigns/")

        assert response.status_code == 200
        data = response.json()
        assert len(data) == 2
        assert data[0]["title"] == "Test Campaign 1"
        assert data[1]["title"] == "Test Campaign 2"
