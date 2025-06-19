from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.db import crud, schemas
from app.core.security import get_current_user
from typing import List, Optional, Any, Dict

router = APIRouter()

@router.get("/", response_model=List[schemas.QuestOut])
def get_quests(
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1, le=100),
    difficulty_id: Optional[int] = Query(None),
    interest_id: Optional[int] = Query(None),
    quest_type_id: Optional[int] = Query(None),
    is_public: Optional[bool] = Query(None),
    db: Session = Depends(get_db)
) -> List[schemas.QuestOut]:
    filters = {}
    if difficulty_id is not None:
        filters['difficulty_id'] = difficulty_id
    if interest_id is not None:
        filters['interest_id'] = interest_id
    if quest_type_id is not None:
        filters['quest_type_id'] = quest_type_id
    if is_public is not None:
        filters['is_public'] = is_public
    
    quests = crud.get_quests(db, skip=skip, limit=limit, **filters)
    return [schemas.QuestOut.model_validate(quest) for quest in quests]

@router.get("/{quest_id}", response_model=schemas.QuestOut)
def get_quest(quest_id: int, db: Session = Depends(get_db)) -> schemas.QuestOut:
    quest = crud.get_quest(db, quest_id=quest_id)
    if not quest:
        raise HTTPException(status_code=404, detail="Quest not found")
    return schemas.QuestOut.model_validate(quest)

@router.post("/", response_model=schemas.QuestOut)
def create_quest(
    quest_data: schemas.QuestCreate,
    current_user: schemas.UserOut = Depends(get_current_user),
    db: Session = Depends(get_db)
) -> schemas.QuestOut:
    quest = crud.create_quest(db, quest_data, current_user.id)
    return schemas.QuestOut.model_validate(quest)

@router.put("/{quest_id}", response_model=schemas.QuestOut)
def update_quest(
    quest_id: int,
    quest_data: schemas.QuestUpdate,
    current_user: schemas.UserOut = Depends(get_current_user),  # Now this should work
    db: Session = Depends(get_db)
) -> Any:
    quest = crud.get_quest(db, quest_id=quest_id)
    if not quest:
        raise HTTPException(status_code=404, detail="Quest not found")
    
    # Check if user owns the quest or has permission to edit
    if quest.author_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not enough permissions")
    
    updated_quest = crud.update_quest(db, quest_id=quest_id, quest_data=quest_data)
    return updated_quest

@router.post("/{quest_id}/like", response_model=schemas.QuestOut)
def like_quest(quest_id: int, db: Session = Depends(get_db)) -> Any:
    quest = crud.like_quest(db, quest_id=quest_id)
    if not quest:
        raise HTTPException(status_code=404, detail="Quest not found")
    return quest

@router.post("/{quest_id}/bookmark")
def bookmark_quest(
    quest_id: int,
    current_user: schemas.UserOut = Depends(get_current_user),
    db: Session = Depends(get_db)
) -> Dict[str, Any]:
    quest = crud.bookmark_quest(db, quest_id=quest_id)
    if not quest:
        raise HTTPException(status_code=404, detail="Quest not found")
    return {"bookmarks": quest.bookmarks}