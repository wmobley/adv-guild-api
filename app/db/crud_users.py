from sqlalchemy.orm import Session
from sqlalchemy import select
from app.db.models import User, Quest, UserQuestBookmark
from app.db.schemas import UserCreate, UserUpdate
from app.core.security import get_password_hash

def get_user(db: Session, user_id: int) -> User | None:
    return db.query(User).filter(User.id == user_id).first()

def get_user_by_email(db: Session, email: str) -> User | None:
    return db.query(User).filter(User.email == email).first()

def create_user(db: Session, user: UserCreate) -> User:
    # Hash the password here, as UserCreate now takes plain password
    hashed_password = get_password_hash(user.password)
    db_user = User(
        email=user.email,
        display_name=user.display_name,
        hashed_password=hashed_password,
        avatar_url=user.avatar_url,
        guild_rank=user.guild_rank
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def update_user(db: Session, db_user: User, user_in: UserUpdate) -> User:
    # This function needs to be more robust, but for now, just update fields
    # that are present in user_in
    update_data = user_in.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        if key == "password" and value: # Handle password update
            setattr(db_user, "hashed_password", get_password_hash(value))
        else:
            setattr(db_user, key, value)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def get_users(db: Session, skip: int = 0, limit: int = 100) -> list[User]:
    return db.query(User).offset(skip).limit(limit).all()

def get_bookmarked_quests_by_user(db: Session, user_id: int) -> list[Quest]:
    # This query selects Quests that are bookmarked by a specific user.
    # It joins Quest with UserQuestBookmark and filters by user_id.
    return db.query(Quest).join(UserQuestBookmark).filter(UserQuestBookmark.user_id == user_id).all()