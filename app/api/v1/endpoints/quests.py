from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.db import crud_quests, schemas # Changed
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
    quests = crud_quests.get_quests(
        db, skip=skip, limit=limit, difficulty_id=difficulty_id,
        interest_id=interest_id, quest_type_id=quest_type_id, is_public=is_public
    )
    return [schemas.QuestOut.model_validate(quest) for quest in quests]

@router.get("/{quest_id}", response_model=schemas.QuestOut)
def get_quest(quest_id: int, db: Session = Depends(get_db)) -> schemas.QuestOut:
    quest = crud_quests.get_quest(db, quest_id=quest_id) # Changed
    if not quest:
        raise HTTPException(status_code=404, detail="Quest not found")
    return schemas.QuestOut.model_validate(quest)

@router.post("/", response_model=schemas.QuestOut)
def create_quest(
    quest_data: schemas.QuestCreate,
    current_user: schemas.UserOut = Depends(get_current_user),
    db: Session = Depends(get_db)
) -> schemas.QuestOut:
    new_quest = crud_quests.create_quest(db, quest_data, current_user.id)
    db.commit()
    db.refresh(new_quest)
    return schemas.QuestOut.model_validate(new_quest)

@router.put("/{quest_id}", response_model=schemas.QuestOut)
def update_quest(
    quest_id: int,
    quest_data: schemas.QuestUpdate,
    current_user: schemas.UserOut = Depends(get_current_user),  # Now this should work
    db: Session = Depends(get_db)
) -> schemas.QuestOut:
    quest = crud_quests.get_quest(db, quest_id=quest_id) # Changed
    if not quest:
        raise HTTPException(status_code=404, detail="Quest not found")
    
    # Check if user owns the quest or has permission to edit
    if quest.author_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not enough permissions")
    
    updated_quest = crud_quests.update_quest(db, db_quest=quest, quest_in=quest_data)
    db.commit()
    db.refresh(updated_quest)
    return schemas.QuestOut.model_validate(updated_quest)

@router.post("/{quest_id}/like", response_model=schemas.QuestOut)
def like_quest(quest_id: int, db: Session = Depends(get_db)) -> schemas.QuestOut:
    quest = crud_quests.like_quest(db, quest_id=quest_id) # Changed
    if not quest:
        raise HTTPException(status_code=404, detail="Quest not found")
    db.commit()
    db.refresh(quest)
    return schemas.QuestOut.model_validate(quest)

@router.post("/{quest_id}/bookmark")
def bookmark_quest(
    quest_id: int,
    current_user: schemas.UserOut = Depends(get_current_user),
    db: Session = Depends(get_db)
) -> Dict[str, Any]:
    # Check if already bookmarked
    existing_bookmark = crud_quests.get_quest_bookmark_by_user_and_quest(db, user_id=current_user.id, quest_id=quest_id)
    
    if existing_bookmark:
        updated_quest = crud_quests.remove_quest_bookmark_for_user(db, user_id=current_user.id, quest_id=quest_id)
    else:
        updated_quest = crud_quests.add_quest_bookmark_for_user(db, user_id=current_user.id, quest_id=quest_id)
    
    if not updated_quest:
        raise HTTPException(status_code=404, detail="Quest not found")
    db.commit()
    db.refresh(updated_quest)
    return {"bookmarks": updated_quest.bookmarks, "user_bookmarked": not existing_bookmark}