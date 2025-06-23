from sqlalchemy.orm import Session
from typing import Optional, List

from app.core.hashing import get_password_hash, verify_password
from app.db import models, schemas


def get_user(db: Session, user_id: int) -> Optional[models.User]:
    return db.query(models.User).filter(models.User.id == user_id).first()


def get_user_by_email(db: Session, email: str) -> Optional[models.User]:
    return db.query(models.User).filter(models.User.email == email).first()


def get_users(db: Session, skip: int = 0, limit: int = 100) -> List[models.User]:
    return db.query(models.User).offset(skip).limit(limit).all()


def create_user(db: Session, user: schemas.UserCreate) -> models.User:
    hashed_password = get_password_hash(user.password)
    db_user = models.User(
        email=user.email,
        display_name=user.display_name,
        hashed_password=hashed_password,
        avatar_url=user.avatar_url,
        guild_rank=user.guild_rank
    )
    db.add(db_user)
    return db_user


def update_user(db: Session, db_user: models.User, user_in: schemas.UserUpdate) -> models.User:
    update_data = user_in.model_dump(exclude_unset=True)
    if "password" in update_data and update_data["password"]:
        hashed_password = get_password_hash(update_data["password"])
        db_user.hashed_password = hashed_password  # type: ignore [assignment]
        del update_data["password"]

    for key, value in update_data.items():
        setattr(db_user, key, value)

    db.add(db_user)
    return db_user


def authenticate_user(db: Session, email: str, password: str) -> Optional[models.User]:
    user = get_user_by_email(db, email=email)
    if not user:
        return None
    if not verify_password(password, user.hashed_password):  # type: ignore [arg-type]
        return None
    return user


def get_bookmarked_quests_by_user(db: Session, user_id: int) -> List[models.Quest]:
    return db.query(models.Quest).join(models.UserQuestBookmark).filter(models.UserQuestBookmark.user_id == user_id).all()