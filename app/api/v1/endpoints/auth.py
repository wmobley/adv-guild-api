from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.db import crud, schemas
from app.core.security import create_access_token

router = APIRouter()


@router.post("/register", response_model=schemas.UserResponse)
def register(user_data: schemas.UserCreate, db: Session = Depends(get_db)):
    if user_data.email:
        db_user = crud.get_user_by_email(db, email=user_data.email)
        if db_user:
            raise HTTPException(
                status_code=400,
                detail="Email already registered"
            )
    
    user = crud.create_user(db=db, user=user_data)
    access_token = create_access_token(data={"sub": str(user.id)})
    
    return schemas.UserResponse(
        user=user,
        access_token=access_token,
        token_type="bearer"
    )


@router.post("/login", response_model=schemas.UserResponse)
def login(login_data: schemas.UserLogin, db: Session = Depends(get_db)):
    user = crud.get_user_by_email(db, email=login_data.email)
    if not user:
        raise HTTPException(
            status_code=404,
            detail="User not found"
        )
    
    access_token = create_access_token(data={"sub": str(user.id)})
    return schemas.UserResponse(
        user=user,
        access_token=access_token,
        token_type="bearer"
    )