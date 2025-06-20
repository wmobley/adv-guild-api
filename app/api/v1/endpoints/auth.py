from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.db import crud_users, schemas
from app.core.security import create_access_token, verify_password, get_password_hash
from app.db.models import User # Import User model for type hinting
from typing import List, Any, Optional, Dict


router = APIRouter()


def authenticate_user(db: Session, email: str, password: str) -> User | None:
    """Authenticate a user by email and password"""
    user = crud_users.get_user_by_email(db, email=email)
    if not user:
        return None
    if not verify_password(password, user.hashed_password):  # type: ignore[arg-type]
        return None
    return user


@router.post("/register", response_model=schemas.UserResponse)
def register(
    user_data: schemas.UserCreate,
    db: Session = Depends(get_db)
) -> schemas.UserResponse:
    existing_user = crud_users.get_user_by_email(db, email=user_data.email)
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )
    
    user = crud_users.create_user(db, user_data)
    access_token = create_access_token(data={"sub": user.email or str(user.id)})
    user_out = schemas.UserOut.model_validate(user)
    return schemas.UserResponse(
        user=user_out,
        access_token=access_token,
        token_type="bearer"
    )


@router.post("/login", response_model=schemas.UserResponse)
def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
) -> schemas.UserResponse:
    user = authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token = create_access_token(data={"sub": user.email or str(user.id)})
    user_out = schemas.UserOut.model_validate(user)
    return schemas.UserResponse(
        user=user_out,
        access_token=access_token,
        token_type="bearer"
    )


# Simple email-only login for development
@router.post("/login-email", response_model=schemas.UserResponse)
def login_email(
    user_login: schemas.UserLogin,
    db: Session = Depends(get_db)
) -> schemas.UserResponse:
    """Simple email-only login for development purposes"""
    user = crud_users.get_user_by_email(db, email=user_login.email) # Changed
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found"
        )
    
    access_token = create_access_token(data={"sub": user.email})
    user_out = schemas.UserOut.model_validate(user)
    return schemas.UserResponse(
        user=user_out,
        access_token=access_token,
        token_type="bearer"
    )