from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List
from app.db.database import get_db
from app.db import crud, schemas
from app.core.security import get_current_user

router = APIRouter()


@router.get("/me", response_model=schemas.UserOut)
def get_current_user_info(current_user: schemas.UserOut = Depends(get_current_user)):
    return current_user


@router.get("/", response_model=List[schemas.UserOut])
def get_users(
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1, le=100),
    db: Session = Depends(get_db)
):
    users = crud.get_users(db, skip=skip, limit=limit)
    return users


@router.get("/{user_id}", response_model=schemas.UserOut)
def get_user(user_id: int, db: Session = Depends(get_db)):
    user = crud.get_user(db, user_id=user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


@router.put("/me", response_model=schemas.UserOut)
def update_current_user(
    user_data: schemas.UserUpdate,
    current_user: schemas.UserOut = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    # Update user logic would go here
    return current_user