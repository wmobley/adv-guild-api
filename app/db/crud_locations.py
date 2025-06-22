from sqlalchemy.orm import Session
from typing import List, Optional
from app.db.models import Location
from app.db.schemas import LocationCreate, LocationUpdate


def create_location(db: Session, location: LocationCreate) -> Location:
    db_location = Location(**location.model_dump())
    db.add(db_location)
    return db_location


def get_location(db: Session, location_id: int) -> Optional[Location]:
    return db.query(Location).filter(Location.id == location_id).first()


def get_locations(db: Session, skip: int = 0, limit: int = 100) -> List[Location]:
    return db.query(Location).offset(skip).limit(limit).all()


def update_location(db: Session, db_location: Location, location_in: LocationUpdate) -> Location:
    update_data = location_in.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_location, key, value)
    db.add(db_location)
    return db_location


def delete_location(db: Session, location_id: int) -> Optional[Location]:
    db_location = get_location(db, location_id)
    if db_location:
        db.delete(db_location)
        return db_location
    return None