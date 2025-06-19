import pytest
from datetime import datetime
from unittest.mock import patch, Mock # Import Mock
from fastapi.testclient import TestClient
from app.main import app
from app.db import schemas # Keep this if used, otherwise remove
from typing import Dict, Any, List # For type hints
from types import SimpleNamespace

client = TestClient(app) # Correct: app is a positional argument

# Update your mock quest data to match the QuestOut schema
def create_mock_quest_data() -> Dict[str, Any]:
    return {
        "id": 1,
        "name": "Test Quest",  # Changed from title
        "synopsis": "A test quest description",  # Changed from description
        "itinerary": "1. Go here. 2. Do that.", # Added required field
        "author_id": 1,
        "start_location_id": 1,
        "destination_id": 2,
        "interest_id": 1,
        "difficulty_id": 1,
        "quest_type_id": 1,
        "campaign_id": 1, # This is in QuestBase
        # "likes" and "bookmarks" are not in QuestOut schema, remove if not intended in response
        # For from_attributes=True with model_validate, use actual datetime objects
        "created_at": datetime.now(),
        "updated_at": datetime.now(), # Or None
        "is_public": True, # from QuestBase
        # Nested objects
        "author": {
            "id": 1,
            "display_name": "Test User",
            "email": "test@example.com",
            "avatar_url": None,
            "guild_rank": "Novice"
        },
        "start_location": {
            "id": 1,
            "name": "Start Location",
            "description": "Starting point",
            "latitude": 40.7128,
            "longitude": -74.0060
        },
        "destination": {
            "id": 2,
            "name": "Destination",
            "description": "End point",
            "latitude": 41.8781,
            "longitude": -87.6298
        },
        "interest": {
            "id": 1,
            "name": "Combat"
        },
        "difficulty": {
            "id": 1,
            "name": "Novice"
        },
        "quest_type": {
            "id": 1,
            "name": "Dungeon Crawl"
        },
        "campaign": {
            "id": 1,
            "title": "Test Campaign",
            "description": "A test campaign",
            "author_id": 1
        }
    }

def create_mock_quest_object(quest_data: Dict[str, Any]) -> SimpleNamespace:
    """Create a mock quest object with nested objects"""
    mock_quest = SimpleNamespace(**quest_data)
    
    # Create nested SimpleNamespace objects
    mock_quest.author = SimpleNamespace(**quest_data["author"])
    mock_quest.start_location = SimpleNamespace(**quest_data["start_location"])
    mock_quest.destination = SimpleNamespace(**quest_data["destination"])
    mock_quest.interest = SimpleNamespace(**quest_data["interest"])
    mock_quest.difficulty = SimpleNamespace(**quest_data["difficulty"])
    mock_quest.quest_type = SimpleNamespace(**quest_data["quest_type"])
    mock_quest.campaign = SimpleNamespace(**quest_data["campaign"])
    
    return mock_quest

# Update your test functions to use proper mock data
@patch('app.db.crud.get_quests')
def test_get_quests_success(mock_get_quests: Mock, client: TestClient) -> None:
    mock_quest_data = create_mock_quest_data()
    mock_quest = create_mock_quest_object(mock_quest_data)
    
    mock_get_quests.return_value = [mock_quest]
    
    response = client.get("/api/v1/quests/")
    
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
    assert data[0]["id"] == 1
    assert data[0]["name"] == "Test Quest"

@patch('app.db.crud.get_quests')
def test_get_quests_with_filters(mock_get_quests: Mock, client: TestClient) -> None:
    mock_quest_data = create_mock_quest_data()
    mock_quest = SimpleNamespace(**mock_quest_data)
    
    # Set up nested objects
    mock_quest.author = SimpleNamespace(**mock_quest_data["author"])
    mock_quest.start_location = SimpleNamespace(**mock_quest_data["start_location"])
    mock_quest.destination = SimpleNamespace(**mock_quest_data["destination"])
    mock_quest.interest = SimpleNamespace(**mock_quest_data["interest"])
    mock_quest.difficulty = SimpleNamespace(**mock_quest_data["difficulty"])
    mock_quest.quest_type = SimpleNamespace(**mock_quest_data["quest_type"])
    mock_quest.campaign = SimpleNamespace(**mock_quest_data["campaign"])
    
    mock_get_quests.return_value = [mock_quest]
    
    response = client.get("/api/v1/quests/?difficulty_id=1&quest_type_id=1")
    
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1

@patch('app.db.crud.get_quests')
def test_get_quests_pagination(mock_get_quests: Mock, client: TestClient) -> None:
    # Create multiple mock quests
    mock_quests = []
    for i in range(3):
        mock_quest_data = create_mock_quest_data()
        mock_quest_data["id"] = i + 1
        mock_quest_data["name"] = f"Test Quest {i + 1}"
        
        mock_quest = SimpleNamespace(**mock_quest_data)
        mock_quest.author = SimpleNamespace(**mock_quest_data["author"])
        mock_quest.start_location = SimpleNamespace(**mock_quest_data["start_location"])
        mock_quest.destination = SimpleNamespace(**mock_quest_data["destination"])
        mock_quest.interest = SimpleNamespace(**mock_quest_data["interest"])
        mock_quest.difficulty = SimpleNamespace(**mock_quest_data["difficulty"])
        mock_quest.quest_type = SimpleNamespace(**mock_quest_data["quest_type"])
        mock_quest.campaign = SimpleNamespace(**mock_quest_data["campaign"])
        
        mock_quests.append(mock_quest)
    
    mock_get_quests.return_value = mock_quests[:2]  # Return first 2 for pagination
    
    response = client.get("/api/v1/quests/?skip=0&limit=2")
    
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 2

@patch('app.db.crud.get_quests')
def test_get_quests_empty(mock_get_quests: Mock, client: TestClient) -> None:
    mock_get_quests.return_value = []
    
    response = client.get("/api/v1/quests/")
    
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 0
