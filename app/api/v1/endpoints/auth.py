from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.db import crud, schemas
from app.core.security import create_access_token, verify_password, get_password_hash
from typing import List, Any, Optional, Dict  # Add Dict if needed


router = APIRouter()


def authenticate_user(db: Session, email: str, password: str) -> schemas.UserOut | None:
    """Authenticate a user by email and password"""
    user = crud.get_user_by_email(db, email=email)
    if not user:
        return None
    
    # If you have password field in your user model:
    # if not verify_password(password, user.hashed_password):
    #     return None
    
    # For now, since your schema doesn't seem to have passwords,
    # we'll just return the user (THIS IS NOT SECURE - implement passwords!)
    return schemas.UserOut.model_validate(user)


@router.post("/register", response_model=schemas.UserResponse)
def register(
    user_data: schemas.UserCreate,
    db: Session = Depends(get_db)
) -> schemas.UserResponse:
    # Check if user already exists
    if user_data.email:
        existing_user = crud.get_user_by_email(db, email=user_data.email)
        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email already registered"
            )
    
    user = crud.create_user(db, user_data)
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
    return schemas.UserResponse(
        user=user,
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
    user = crud.get_user_by_email(db, email=user_login.email)
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