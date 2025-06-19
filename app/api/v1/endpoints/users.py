from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.db import crud, schemas
from app.core.security import get_current_user
from typing import List

router = APIRouter()

@router.get("/", response_model=List[schemas.UserOut])
def get_users(
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1, le=100),
    db: Session = Depends(get_db)
) -> List[schemas.UserOut]:
    users = crud.get_users(db, skip=skip, limit=limit)
    return [schemas.UserOut.model_validate(user) for user in users]

@router.get("/me", response_model=schemas.UserOut)
def get_current_user_info(
    current_user: schemas.UserOut = Depends(get_current_user)
) -> schemas.UserOut:
    return current_user

@router.put("/me", response_model=schemas.UserOut)
def update_current_user(
    user_update: schemas.UserUpdate,
    current_user: schemas.UserOut = Depends(get_current_user),
    db: Session = Depends(get_db)
) -> schemas.UserOut:
    # Example of an explicit 403 check: Prevent inactive users from updating
    if not current_user.is_active:
        raise HTTPException(status_code=403, detail="Inactive users cannot update their profile.")

    updated_user = crud.update_user(db, current_user.id, user_update)
    if not updated_user:
        raise HTTPException(status_code=404, detail="User not found")
    return schemas.UserOut.model_validate(updated_user)

@router.get("/{user_id}", response_model=schemas.UserOut)
def get_user(user_id: int, db: Session = Depends(get_db)) -> schemas.UserOut:
    if user_id <= 0:
        raise HTTPException(status_code=422, detail="User ID must be positive")
    
    user = crud.get_user(db, user_id=user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return schemas.UserOut.model_validate(user)