import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from app.db import models
from app.core.password import get_password_hash
from app.core.security import create_access_token


class TestUsersEndpoint:
    """Test class for users endpoint"""
    
    def test_get_users_empty(self, client: TestClient) -> None:
        """Test getting users when database is empty"""
        response = client.get("/api/v1/users/")
        assert response.status_code == 200
        assert response.json() == []

    def test_get_users_with_pagination(self, client: TestClient, db: Session) -> None:
        """Test getting users with pagination parameters"""
        # Create test users
        users = []
        for i in range(15):
            user = models.User(
                email=f"user{i}@example.com",
                display_name=f"User {i}",
                hashed_password=get_password_hash("password123")
            )
            users.append(user)
            db.add(user)
        db.commit()
        
        # Test default pagination
        response = client.get("/api/v1/users/")
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 10  # Default limit
        
        # Test custom pagination
        response = client.get("/api/v1/users/?skip=5&limit=5")
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 5

    def test_get_user_by_id(self, client: TestClient, db: Session) -> None:
        """Test getting a specific user by ID"""
        # Create test user
        user = models.User(
            email="test@example.com",
            display_name="Test User",
            hashed_password=get_password_hash("password123")
        )
        db.add(user)
        db.commit()
        db.refresh(user)
        
        response = client.get(f"/api/v1/users/{user.id}")
        assert response.status_code == 200
        data = response.json()
        assert data["email"] == "test@example.com"
        assert data["display_name"] == "Test User"

    def test_get_user_not_found(self, client: TestClient) -> None:
        """Test getting a user that doesn't exist"""
        response = client.get("/api/v1/users/999")
        assert response.status_code == 404
        assert response.json()["detail"] == "User not found"

    def test_get_current_user_info(self, client: TestClient, db: Session) -> None:
        """Test getting current user info"""
        # Create test user
        user = models.User(
            email="current@example.com",
            display_name="Current User",
            hashed_password=get_password_hash("password123"),
            is_active=True
        )
        db.add(user)
        db.commit()
        db.refresh(user)
        
        # Create access token
        access_token = create_access_token(data={"sub": user.email})
        
        response = client.get(
            "/api/v1/users/me",
            headers={"Authorization": f"Bearer {access_token}"}
        )
        assert response.status_code == 200
        data = response.json()
        assert data["email"] == "current@example.com"
        assert data["display_name"] == "Current User"

    def test_get_current_user_unauthorized(self, client: TestClient) -> None:
        """Test getting current user info without authentication"""
        response = client.get("/api/v1/users/me")
        assert response.status_code == 401

    def test_update_current_user_inactive(self, client: TestClient, db: Session) -> None:
        """Test updating profile as inactive user"""
        # Create inactive test user
        user = models.User(
            email="inactive@example.com",
            display_name="Inactive User",
            hashed_password=get_password_hash("password123"),
            is_active=False
        )
        db.add(user)
        db.commit()
        db.refresh(user)
        
        # Create access token
        access_token = create_access_token(data={"sub": user.email})
        
        update_data = {"display_name": "New Name"}
        
        response = client.put(
            "/api/v1/users/me",
            json=update_data,
            headers={"Authorization": f"Bearer {access_token}"}
        )
        assert response.status_code == 403
        assert response.json()["detail"] == "Inactive users cannot update their profile."

    def test_get_user_invalid_id(self, client: TestClient) -> None:
        """Test getting user with invalid ID format"""
        response = client.get("/api/v1/users/0")
        assert response.status_code == 422  # Validation error for ID <= 0
        
        response = client.get("/api/v1/users/-1")
        assert response.status_code == 422  # Validation error for negative ID

    def test_get_users_invalid_pagination(self, client: TestClient) -> None:
        """Test getting users with invalid pagination parameters"""
        # Test negative skip
        response = client.get("/api/v1/users/?skip=-1")
        assert response.status_code == 422
        
        # Test invalid limit (too high)
        response = client.get("/api/v1/users/?limit=101")
        assert response.status_code == 422
        
        # Test invalid limit (too low)
        response = client.get("/api/v1/users/?limit=0")
        assert response.status_code == 422

    def test_get_my_bookmarked_quests_unauthorized(self, client: TestClient) -> None:
        """Test getting bookmarked quests without authentication"""
        response = client.get("/api/v1/users/me/bookmarks")
        assert response.status_code == 401