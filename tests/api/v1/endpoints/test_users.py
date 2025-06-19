import pytest
from datetime import datetime, timezone # Import timezone
from unittest.mock import Mock, patch
from fastapi.testclient import TestClient
from fastapi import HTTPException
from typing import Dict, Any, List
from app.main import app
from app.db import schemas  # Import schemas
from app.core.security import get_current_user as original_get_current_user # Import the original dependency
from typing import Dict, Any, List
from types import SimpleNamespace

client = TestClient(app) # Correct: app is a positional argument

def create_mock_user_data() -> Dict[str, Any]:
    now_utc = datetime.now(timezone.utc) # Create a timezone-aware datetime
    return {
        "id": 1,
        "display_name": "Test User", # Matches models.User and schemas.UserBase
        "email": "test@example.com",
        "avatar_url": None, # Matches models.User and schemas.UserBase
        "guild_rank": "Novice", # Matches models.User and schemas.UserBase
        "is_active": True,  # Added: UserOut expects this (though it has a default)
        "created_at": now_utc,  # Use timezone-aware datetime
        "updated_at": now_utc   # Use timezone-aware datetime (or None if appropriate for your schema)
    }

def create_mock_user_object_for_orm() -> SimpleNamespace:
    """Create a mock user object that mimics a SQLAlchemy model instance."""
    data = create_mock_user_data()
    # Create a SimpleNamespace with attributes matching models.User fields
    mock_user = SimpleNamespace(
        id=data["id"],
        display_name=data["display_name"],
        email=data["email"],
        avatar_url=data["avatar_url"],
        guild_rank=data["guild_rank"],
        is_active=data["is_active"],
        created_at=data["created_at"],
        updated_at=data["updated_at"],
    )
    return mock_user

@patch('app.db.crud.get_user')
def test_get_user_success(mock_get_user: Mock, client: TestClient) -> None:  # Use Mock instead of patch
    # Create mock user with all required fields
    mock_user_data = create_mock_user_data()
    mock_user = SimpleNamespace(**mock_user_data)
    
    mock_get_user.return_value = mock_user
    
    response = client.get("/api/v1/users/1")
    
    assert response.status_code == 200
    data = response.json() # This will be UserOut serialized
    assert data["id"] == 1
    assert data["display_name"] == "Test User"  # Use display_name
    assert data["email"] == "test@example.com"

@patch('app.db.crud.get_users')
def test_get_users_success(mock_get_users: Mock, client: TestClient) -> None:  # Use Mock instead of patch
    # Create multiple mock users
    mock_users = []
    for i in range(3):
        user_data = create_mock_user_data()
        user_data["id"] = i + 1
        user_data["display_name"] = f"Test User {i+1}"
        user_data["email"] = f"test{i + 1}@example.com"
        
        mock_user = SimpleNamespace(**user_data)
        mock_users.append(mock_user)
    
    mock_get_users.return_value = mock_users
    
    response = client.get("/api/v1/users/")
    
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 3
    assert data[0]["display_name"] == "Test User 1"  # Use display_name


def test_get_current_user_info(client: TestClient) -> None:
    # Mock the current user
    mock_user_object = create_mock_user_object_for_orm() # This returns a SimpleNamespace (ORM-like)
    
    # Override the dependency
    app.dependency_overrides[original_get_current_user] = lambda: mock_user_object
    try:
        # Add Authorization header
        response = client.get("/api/v1/users/me", headers={"Authorization": "Bearer testtoken"})
        
        assert response.status_code == 200
        data = response.json()
        assert data["id"] == 1
        assert data["display_name"] == mock_user_object.display_name # Verify against mock object
        assert data["email"] == mock_user_object.email # Verify more fields
    finally:
        app.dependency_overrides.clear() # Clear overrides after the test


@patch('app.api.v1.endpoints.users.crud.update_user') # Patch crud where it's used by the endpoint
def test_update_current_user(mock_crud_update_user: Mock, client: TestClient) -> None:  # Use Mock instead of patch
    # Mock current user
    # get_current_user returns an ORM-like object, FastAPI converts it to schemas.UserOut
    mock_current_orm_user = create_mock_user_object_for_orm()

    # Override the dependency
    app.dependency_overrides[original_get_current_user] = lambda: mock_current_orm_user
    
    # Mock updated user
    # crud.update_user returns a models.User instance. Mock this with SimpleNamespace.
    base_user_data_for_update = create_mock_user_data() # Get a fresh mock data dict
    base_user_data_for_update['id'] = mock_current_orm_user.id # Ensure ID matches the current user
    updated_user_model_mock_data = {**base_user_data_for_update, "display_name": "Updated Name"}
    updated_user_model_mock = SimpleNamespace(**updated_user_model_mock_data)
    
    mock_crud_update_user.return_value = updated_user_model_mock
    
    update_data = {"display_name": "Updated Name"} # This matches UserUpdate schema now
    
    # Add Authorization header
    response = client.put("/api/v1/users/me", json=update_data, headers={"Authorization": "Bearer testtoken"})
    
    if response.status_code != 200:
        print(f"Unexpected response status: {response.status_code}, content: {response.text}")

    try:
        assert response.status_code == 200
        data = response.json()
        assert data["display_name"] == "Updated Name"
        assert data["id"] == updated_user_model_mock.id # Check ID consistency (should match the updated mock)
    finally:
        app.dependency_overrides.clear() # Clear overrides after the test

def test_get_user_not_found(client: TestClient) -> None: # Added type annotation
    with patch("app.db.crud.get_user") as mock_get_user:
        mock_get_user.return_value = None
        
        response = client.get("/api/v1/users/999")
        
        assert response.status_code == 404
        assert response.json()["detail"] == "User not found"

def test_get_user_invalid_id(client: TestClient) -> None: # Added type annotation
    response = client.get("/api/v1/users/invalid")
    assert response.status_code == 422

def test_get_user_negative_id(client: TestClient) -> None: # Added type annotation
    response = client.get("/api/v1/users/-1")
    
    # FastAPI validation returns 422 for invalid input types
    assert response.status_code == 422
    assert "detail" in response.json() # Using response.json() directly
