from fastapi import APIRouter, Depends, HTTPException, Query, Path
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.db import crud_users, schemas, models, crud_quests
from app.core.security import get_current_user
from typing import List, cast

router = APIRouter()

@router.get("/", response_model=List[schemas.UserOut])
def get_users(
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1, le=100),
    db: Session = Depends(get_db)
) -> List[schemas.UserOut]:
    users = crud_users.get_users(db, skip=skip, limit=limit) # Changed
    return [schemas.UserOut.model_validate(user) for user in users]

@router.get("/me/", response_model=schemas.UserOut)
def get_current_user_info(
    current_user: models.User = Depends(get_current_user)
) -> schemas.UserOut:
    return schemas.UserOut.model_validate(current_user)

@router.put("/me/", response_model=schemas.UserOut)
def update_current_user(
    user_update: schemas.UserUpdate,
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db)
) -> schemas.UserOut:
    # Example of an explicit 403 check: Prevent inactive users from updating
    if not current_user.is_active:
        raise HTTPException(status_code=403, detail="Inactive users cannot update their profile.")

    updated_user = crud_users.update_user(db, current_user, user_update) # Pass the User object
    db.commit()
    db.refresh(updated_user)
    return schemas.UserOut.model_validate(updated_user)

@router.get("/{user_id}/", response_model=schemas.UserOut)
def get_user(
    user_id: int = Path(..., gt=0, description="The ID of the user to retrieve."),
    db: Session = Depends(get_db)
) -> schemas.UserOut:
    user = crud_users.get_user(db, user_id=user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return schemas.UserOut.model_validate(user)

@router.get("/me/bookmarks/", response_model=List[schemas.QuestOut]) # Assuming you want to return a list of Quests
def get_my_bookmarked_quests(
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db)
) -> List[schemas.QuestOut]:
    """
    Retrieve all quests bookmarked by the current user.
    """
    bookmarked_quests = crud_users.get_bookmarked_quests_by_user(db, user_id=cast(int, current_user.id))
    return [schemas.QuestOut.model_validate(quest) for quest in bookmarked_quests]


@router.get("/me/quests/", response_model=List[schemas.QuestOut])
def get_my_quests(
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1, le=100),
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db)
) -> List[schemas.QuestOut]:
    """
    Retrieve all quests created by the current user.
    """
    quests = crud_quests.get_quests(db, author_id=cast(int, current_user.id), skip=skip, limit=limit)
    return [schemas.QuestOut.model_validate(quest) for quest in quests]