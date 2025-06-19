from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from app.db.database import get_db
from app.db import crud, schemas
from app.core.security import get_current_user

router = APIRouter()


@router.get("/", response_model=schemas.QuestListResponse)
def get_quests(
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1, le=100),
    is_public: Optional[bool] = Query(None),
    difficulty_id: Optional[int] = Query(None),
    interest_id: Optional[int] = Query(None),
    db: Session = Depends(get_db)
):
    quests, total = crud.get_quests(
        db, 
        skip=skip, 
        limit=limit,
        is_public=is_public,
        difficulty_id=difficulty_id,
        interest_id=interest_id
    )
    
    return schemas.QuestListResponse(
        quests=quests,
        total=total,
        skip=skip,
        limit=limit
    )


@router.post("/", response_model=schemas.QuestOut)
def create_quest(
    quest_data: schemas.QuestCreate,
    current_user: schemas.UserOut = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    return crud.create_quest(db=db, quest=quest_data, author_id=current_user.id)


@router.get("/{quest_id}", response_model=schemas.QuestOut)
def get_quest(quest_id: int, db: Session = Depends(get_db)):
    quest = crud.get_quest(db, quest_id=quest_id)
    if not quest:
        raise HTTPException(status_code=404, detail="Quest not found")
    return quest


@router.put("/{quest_id}", response_model=schemas.QuestOut)
def update_quest(
    quest_id: int,
    quest_data: schemas.QuestUpdate,
    current_user: schemas.UserOut = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    quest = crud.get_quest(db, quest_id=quest_id)
    if not quest:
        raise HTTPException(status_code=404, detail="Quest not found")
    
    if quest.author_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized to update this quest")
    
    return crud.update_quest(db=db, quest_id=quest_id, quest_data=quest_data)


@router.post("/{quest_id}/like")
def like_quest(
    quest_id: int,
    current_user: schemas.UserOut = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    quest = crud.like_quest(db, quest_id=quest_id)
    if not quest:
        raise HTTPException(status_code=404, detail="Quest not found")
    return {"likes": quest.likes}


@router.post("/{quest_id}/bookmark")
def bookmark_quest(
    quest_id: int,
    current_user: schemas.UserOut = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    quest = crud.bookmark_quest(db, quest_id=quest_id)
    if not quest:
        raise HTTPException(status_code=404, detail="Quest not found")
    return {"bookmarks": quest.bookmarks}