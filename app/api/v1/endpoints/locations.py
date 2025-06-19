from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.db import crud, schemas
from app.core.security import get_current_user
from typing import List, Any, Optional, Dict  # Add Dict if needed


router = APIRouter()

@router.get("/", response_model=List[schemas.LocationOut])
def get_locations(
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1, le=100),
    db: Session = Depends(get_db)
) -> List[schemas.LocationOut]:
    locations = crud.get_locations(db, skip=skip, limit=limit)
    return [schemas.LocationOut.from_orm(location) for location in locations]

@router.get("/{location_id}", response_model=schemas.LocationOut)
def get_location(location_id: int, db: Session = Depends(get_db)) -> schemas.LocationOut:
    location = crud.get_location(db, location_id=location_id)
    if not location:
        raise HTTPException(status_code=404, detail="Location not found")
    return schemas.LocationOut.from_orm(location)

@router.post("/", response_model=schemas.LocationOut)
def create_location(
    location_data: schemas.LocationCreate,
    db: Session = Depends(get_db)
) -> schemas.LocationOut:
    location = crud.create_location(db, location_data)
    return schemas.LocationOut.from_orm(location)

@router.put("/{location_id}", response_model=schemas.LocationOut)
def update_location(
    location_id: int,
    location_data: schemas.LocationCreate, # Or a specific LocationUpdate schema if you have one
    db: Session = Depends(get_db)
) -> schemas.LocationOut:
    existing_location = crud.get_location(db, location_id=location_id)
    if not existing_location:
        raise HTTPException(status_code=404, detail="Location not found")
    
    updated_location = crud.update_location(db, location_id=location_id, location_data=location_data)
    if not updated_location: # Should not happen if get_location found it, but good for safety
        raise HTTPException(status_code=404, detail="Location not found during update")
    return schemas.LocationOut.from_orm(updated_location)

@router.delete("/{location_id}", response_model=schemas.LocationOut) # Or just status_code=204 if no body
def delete_location(
    location_id: int,
    db: Session = Depends(get_db)
) -> schemas.LocationOut: # Or return a Dict like {"message": "Location deleted"}
    deleted_location = crud.delete_location(db, location_id=location_id)
    if not deleted_location:
        raise HTTPException(status_code=404, detail="Location not found")
    return schemas.LocationOut.from_orm(deleted_location) # Or return the message