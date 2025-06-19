from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List
from app.db.database import get_db
from app.db import crud, schemas

router = APIRouter()


@router.get("/quest-types", response_model=List[schemas.QuestTypeOut])
def get_quest_types(db: Session = Depends(get_db)):
    return crud.get_quest_types(db)


@router.get("/difficulties", response_model=List[schemas.DifficultyOut])
def get_difficulties(db: Session = Depends(get_db)):
    return crud.get_difficulties(db)


@router.get("/interests", response_model=List[schemas.InterestOut])
def get_interests(db: Session = Depends(get_db)):
    return crud.get_interests(db)