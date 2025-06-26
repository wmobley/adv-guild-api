import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session
from typing import Dict, Any

from app.core.security import get_password_hash, create_access_token
from app.db import crud_users, models, schemas


def test_get_my_quests(client: TestClient, db: Session, sample_reference_data: Dict[str, Any]) -> None:
    """Test getting quests created by the current user."""
    # Create a user
    user1 = models.User(
        email="user1@example.com",
        display_name="User One",
        hashed_password=get_password_hash("password123"),
        is_active=True
    )
    # Create another user
    user2 = models.User(
        email="user2@example.com",
        display_name="User Two",
        hashed_password=get_password_hash("password123"),
        is_active=True
    )
    db.add_all([user1, user2])
    db.commit()
    db.refresh(user1)
    db.refresh(user2)

    # Use the reference data from the fixture
    quest_type = sample_reference_data['quest_type']
    difficulty = sample_reference_data['difficulty']
    interest = sample_reference_data['interest']
    location = sample_reference_data['location']
    
    db.add_all([quest_type, difficulty, interest, location])
    db.commit()
    db.refresh(quest_type)
    db.refresh(difficulty)
    db.refresh(interest)
    db.refresh(location)

    # Create quests with all required fields
    quest1 = models.Quest(
        name="Quest 1 by User 1",
        author_id=user1.id,
        synopsis="Test synopsis 1",
        start_location_id=location.id,
        interest_id=interest.id,
        itinerary="Test itinerary 1",
        difficulty_id=difficulty.id,
        quest_type_id=quest_type.id
    )
    quest2 = models.Quest(
        name="Quest 2 by User 1",
        author_id=user1.id,
        synopsis="Test synopsis 2",
        start_location_id=location.id,
        interest_id=interest.id,
        itinerary="Test itinerary 2",
        difficulty_id=difficulty.id,
        quest_type_id=quest_type.id
    )
    quest3 = models.Quest(
        name="Quest 3 by User 2",
        author_id=user2.id,
        synopsis="Test synopsis 3",
        start_location_id=location.id,
        interest_id=interest.id,
        itinerary="Test itinerary 3",
        difficulty_id=difficulty.id,
        quest_type_id=quest_type.id
    )
    db.add_all([quest1, quest2, quest3])
    db.commit()

    # Get access token for user1
    access_token = create_access_token(data={"sub": user1.email})
    headers = {"Authorization": f"Bearer {access_token}"}

    # Make request to get user1's quests
    response = client.get("/api/v1/users/me/quests", headers=headers)
    assert response.status_code == 200
    data = response.json()
    
    assert len(data) == 2
    quest_names = {q["name"] for q in data}
    assert "Quest 1 by User 1" in quest_names
    assert "Quest 2 by User 1" in quest_names
    assert "Quest 3 by User 2" not in quest_names


def test_get_my_quests_unauthorized(client: TestClient) -> None:
    """Test getting my quests without authentication."""
    response = client.get("/api/v1/users/me/quests")
    assert response.status_code == 401


def test_get_my_quests_empty(client: TestClient, db: Session) -> None:
    """Test getting my quests when user has created none."""
    # Create a user
    user = models.User(
        email="noquests@example.com",
        display_name="No Quests User",
        hashed_password=get_password_hash("password123"),
        is_active=True
    )
    db.add(user)
    db.commit()
    db.refresh(user)

    # Get access token
    access_token = create_access_token(data={"sub": user.email})
    headers = {"Authorization": f"Bearer {access_token}"}

    # Make request
    response = client.get("/api/v1/users/me/quests", headers=headers)
    assert response.status_code == 200
    assert response.json() == []