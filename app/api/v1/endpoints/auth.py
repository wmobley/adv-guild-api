from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app.db import crud_users, schemas
from app.db.database import get_db
from app.core import security
from typing import Dict, Any

router = APIRouter()


@router.post("/login/", response_model=schemas.UserResponse)
def login_for_access_token(
    db: Session = Depends(get_db), form_data: OAuth2PasswordRequestForm = Depends()
) -> Dict[str, Any]:
    user = crud_users.authenticate_user(
        db, email=form_data.username, password=form_data.password
    )
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token = security.create_access_token(data={"sub": user.email})
    return {
        "user": schemas.UserOut.model_validate(user),
        "access_token": access_token,
        "token_type": "bearer",
    }


@router.post("/register/", response_model=schemas.UserResponse)
def register_user(user_in: schemas.UserCreate, db: Session = Depends(get_db)) -> Dict[str, Any]:
    db_user = crud_users.get_user_by_email(db, email=user_in.email)
    if db_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Email already registered"
        )
    new_user = crud_users.create_user(db=db, user=user_in)
    db.commit()
    db.refresh(new_user)
    access_token = security.create_access_token(data={"sub": new_user.email})
    return {
        "user": schemas.UserOut.model_validate(new_user),
        "access_token": access_token,
        "token_type": "bearer",
    }