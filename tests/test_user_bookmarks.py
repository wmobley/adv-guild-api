import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from app.db import models
from app.core.security import get_password_hash, create_access_token


def test_get_my_bookmarked_quests_empty(client: TestClient, db: Session) -> None:
    """Test getting bookmarked quests when user has no bookmarks"""
    # Create test user
    user = models.User(
        email="bookmarks@example.com",
        display_name="Bookmark User",
        hashed_password=get_password_hash("password123"),
        is_active=True
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    
    # Create access token
    access_token = create_access_token(data={"sub": user.email})
    
    response = client.get(
        "/api/v1/users/me/bookmarks",
        headers={"Authorization": f"Bearer {access_token}"}
    )
    assert response.status_code == 200
    assert response.json() == []


def test_get_my_bookmarked_quests_unauthorized(client: TestClient) -> None:
    """Test getting bookmarked quests without authentication"""
    response = client.get("/api/v1/users/me/bookmarks")
    assert response.status_code == 401