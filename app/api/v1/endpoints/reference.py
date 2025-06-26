from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError  # Add this import
from app.db.database import get_db
from app.db import crud_reference_data, schemas # Changed
from typing import List

router = APIRouter()

@router.get("/interests/", response_model=List[schemas.InterestOut])
def get_interests(db: Session = Depends(get_db)) -> List[schemas.InterestOut]:
    try:
        interests = crud_reference_data.get_interests(db) # Changed
        return [schemas.InterestOut.model_validate(interest) for interest in interests]
    except SQLAlchemyError:
        raise HTTPException(status_code=500, detail="Database error occurred")

@router.get("/difficulties/", response_model=List[schemas.DifficultyOut])
def get_difficulties(db: Session = Depends(get_db)) -> List[schemas.DifficultyOut]:
    try:
        difficulties = crud_reference_data.get_difficulties(db) # Changed
        return [schemas.DifficultyOut.model_validate(difficulty) for difficulty in difficulties]
    except SQLAlchemyError:
        raise HTTPException(status_code=500, detail="Database error occurred")

@router.get("/quest-types/", response_model=List[schemas.QuestTypeOut])
def get_quest_types(db: Session = Depends(get_db)) -> List[schemas.QuestTypeOut]:
    try:
        quest_types = crud_reference_data.get_quest_types(db) # Changed
        return [schemas.QuestTypeOut.model_validate(quest_type) for quest_type in quest_types]
    except SQLAlchemyError:
        raise HTTPException(status_code=500, detail="Database error occurred")
