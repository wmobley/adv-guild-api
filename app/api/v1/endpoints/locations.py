from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List
from app.db.database import get_db
from app.db import crud, schemas
from app.core.security import get_current_user

router = APIRouter()


@router.get("/", response_model=List[schemas.LocationOut])
def get_locations(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    db: Session = Depends(get_db)
):
    return crud.get_locations(db, skip=skip, limit=limit)


@router.post("/", response_model=schemas.LocationOut)
def create_location(
    location_data: schemas.LocationCreate,
    current_user: schemas.UserOut = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    return crud.create_location(db=db, location=location_data)


@router.get("/{location_id}", response_model=schemas.LocationOut)
def get_location(location_id: int, db: Session = Depends(get_db)):
    location = crud.get_location(db, location_id=location_id)
    if not location:
        raise HTTPException(status_code=404, detail="Location not found")
    return location