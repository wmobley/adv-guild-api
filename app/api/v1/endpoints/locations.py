from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.db import crud_locations, schemas # Changed
from app.core.security import get_current_user
from typing import List, Any, Optional, Dict  # Add Dict if needed


router = APIRouter()

@router.get("/", response_model=List[schemas.LocationOut])
def get_locations(
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1, le=100),
    db: Session = Depends(get_db)
) -> List[schemas.LocationOut]:
    locations = crud_locations.get_locations(db, skip=skip, limit=limit)
    return [schemas.LocationOut.model_validate(location) for location in locations]

@router.get("/{location_id}", response_model=schemas.LocationOut)
def get_location(location_id: int, db: Session = Depends(get_db)) -> schemas.LocationOut:
    location = crud_locations.get_location(db, location_id=location_id)
    if not location:
        raise HTTPException(status_code=404, detail="Location not found")
    return schemas.LocationOut.model_validate(location)

@router.post("/", response_model=schemas.LocationOut)
def create_location(
    location_data: schemas.LocationCreate,
    db: Session = Depends(get_db),
    current_user: schemas.UserOut = Depends(get_current_user)
) -> schemas.LocationOut:
    # NOTE: Authorization check could be added here if needed
    location = crud_locations.create_location(db, location_data)
    return schemas.LocationOut.model_validate(location)

@router.put("/{location_id}", response_model=schemas.LocationOut)
def update_location(
    location_id: int,
    location_data: schemas.LocationUpdate,
    db: Session = Depends(get_db),
    current_user: schemas.UserOut = Depends(get_current_user)
) -> schemas.LocationOut:
    existing_location = crud_locations.get_location(db, location_id=location_id)
    if not existing_location:
        raise HTTPException(status_code=404, detail="Location not found")
    
    # NOTE: Authorization check could be added here, e.g., if locations have authors
    updated_location = crud_locations.update_location(db, db_location=existing_location, location_in=location_data)
    return schemas.LocationOut.model_validate(updated_location)

@router.delete("/{location_id}", response_model=schemas.LocationOut)
def delete_location(
    location_id: int,
    db: Session = Depends(get_db),
    current_user: schemas.UserOut = Depends(get_current_user)
) -> schemas.LocationOut:
    # NOTE: Authorization check could be added here
    deleted_location = crud_locations.delete_location(db, location_id=location_id)
    if not deleted_location:
        raise HTTPException(status_code=404, detail="Location not found")
    return schemas.LocationOut.model_validate(deleted_location)