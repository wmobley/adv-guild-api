from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from typing import List, Optional
from app.db import models, schemas


# User CRUD
def get_user(db: Session, user_id: int) -> Optional[models.User]:
    return db.query(models.User).filter(models.User.id == user_id).first()


def get_user_by_email(db: Session, email: str) -> Optional[models.User]:
    return db.query(models.User).filter(models.User.email == email).first()


def get_users(db: Session, skip: int = 0, limit: int = 100) -> List[models.User]:
    return db.query(models.User).offset(skip).limit(limit).all()


def create_user(db: Session, user: schemas.UserCreate) -> models.User:
    db_user = models.User(**user.model_dump())
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def update_user(db: Session, user_id: int, user_update: schemas.UserUpdate) -> Optional[models.User]:
    db_user = db.query(models.User).filter(models.User.id == user_id).first()
    if db_user:
        for field, value in user_update.model_dump(exclude_unset=True).items():
            setattr(db_user, field, value)
        db.commit()
        db.refresh(db_user)
    return db_user


# Location CRUD
def get_location(db: Session, location_id: int) -> Optional[models.Location]:
    return db.query(models.Location).filter(models.Location.id == location_id).first()


def get_locations(db: Session, skip: int = 0, limit: int = 100) -> List[models.Location]:
    return db.query(models.Location).offset(skip).limit(limit).all()


def create_location(db: Session, location: schemas.LocationCreate) -> models.Location:
    db_location = models.Location(**location.model_dump())
    db.add(db_location)
    db.commit()
    db.refresh(db_location)
    return db_location

def update_location(db: Session, location_id: int, location_data: schemas.LocationCreate) -> Optional[models.Location]:
    db_location = db.query(models.Location).filter(models.Location.id == location_id).first()
    if db_location:
        # Use model_dump to get a dictionary of fields to update
        # exclude_unset=True ensures only provided fields are updated
        update_data = location_data.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_location, field, value)
        db.commit()
        db.refresh(db_location)
    return db_location

def delete_location(db: Session, location_id: int) -> Optional[models.Location]:
    db_location = db.query(models.Location).filter(models.Location.id == location_id).first()
    if db_location:
        db.delete(db_location)
        db.commit()
    return db_location


# Quest CRUD
def get_quest(db: Session, quest_id: int) -> Optional[models.Quest]:
    return db.query(models.Quest).filter(models.Quest.id == quest_id).first()


def get_quests(
    db: Session, 
    skip: int = 0, 
    limit: int = 100,
    difficulty_id: Optional[int] = None,
    quest_type_id: Optional[int] = None,
    interest_id: Optional[int] = None
) -> List[models.Quest]:
    query = db.query(models.Quest)
    
    # Apply filters
    if difficulty_id:
        query = query.filter(models.Quest.difficulty_id == difficulty_id)
    if quest_type_id:
        query = query.filter(models.Quest.quest_type_id == quest_type_id)
    if interest_id:
        query = query.filter(models.Quest.interest_id == interest_id)
    
    # Return just the quests list
    return query.offset(skip).limit(limit).all()

# Or if you want to return both quests and count:
def get_quests_with_count(
    db: Session, 
    skip: int = 0, 
    limit: int = 100,
    difficulty_id: Optional[int] = None,
    quest_type_id: Optional[int] = None,
    interest_id: Optional[int] = None
) -> tuple[List[models.Quest], int]:
    query = db.query(models.Quest)
    
    # Apply filters
    if difficulty_id:
        query = query.filter(models.Quest.difficulty_id == difficulty_id)
    if quest_type_id:
        query = query.filter(models.Quest.quest_type_id == quest_type_id)
    if interest_id:
        query = query.filter(models.Quest.interest_id == interest_id)
    
    total_count = query.count()
    quests = query.offset(skip).limit(limit).all()
    
    return quests, total_count


def create_quest(db: Session, quest: schemas.QuestCreate, author_id: int) -> models.Quest:
    quest_data = quest.model_dump()
    quest_data["author_id"] = author_id
    db_quest = models.Quest(**quest_data)
    db.add(db_quest)
    db.commit()
    db.refresh(db_quest)
    return db_quest


def update_quest(db: Session, quest_id: int, quest_data: schemas.QuestUpdate) -> Optional[models.Quest]:
    db_quest = db.query(models.Quest).filter(models.Quest.id == quest_id).first()
    if db_quest:
        update_data = quest_data.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_quest, field, value)
        db.commit()
        db.refresh(db_quest)
    return db_quest


def like_quest(db: Session, quest_id: int) -> Optional[models.Quest]:
    db_quest = db.query(models.Quest).filter(models.Quest.id == quest_id).first()
    if db_quest:
        # Use setattr to avoid mypy column assignment issues
        current_likes: int = getattr(db_quest, 'likes') or 0
        setattr(db_quest, 'likes', current_likes + 1)
        db.commit()
        db.refresh(db_quest)
    return db_quest


def bookmark_quest(db: Session, quest_id: int) -> Optional[models.Quest]:
    db_quest = db.query(models.Quest).filter(models.Quest.id == quest_id).first()
    if db_quest:
        # Use setattr to avoid mypy column assignment issues
        current_bookmarks: int = getattr(db_quest, 'bookmarks') or 0
        setattr(db_quest, 'bookmarks', current_bookmarks + 1)
        db.commit()
        db.refresh(db_quest)
    return db_quest


# Campaign CRUD
def get_campaign(db: Session, campaign_id: int) -> Optional[models.Campaign]:
    return db.query(models.Campaign).filter(models.Campaign.id == campaign_id).first()


def get_campaigns(db: Session, skip: int = 0, limit: int = 100) -> List[models.Campaign]:
    return db.query(models.Campaign).offset(skip).limit(limit).all()


def create_campaign(db: Session, campaign: schemas.CampaignCreate, author_id: int) -> models.Campaign:
    campaign_data = campaign.model_dump()
    campaign_data["author_id"] = author_id
    db_campaign = models.Campaign(**campaign_data)
    db.add(db_campaign)
    db.commit()
    db.refresh(db_campaign)
    return db_campaign


def update_campaign(db: Session, campaign_id: int, campaign_data: schemas.CampaignUpdate) -> Optional[models.Campaign]:
    db_campaign = db.query(models.Campaign).filter(models.Campaign.id == campaign_id).first()
    if db_campaign:
        update_data = campaign_data.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_campaign, field, value)
        db.commit()
        db.refresh(db_campaign)
    return db_campaign


def delete_campaign(db: Session, campaign_id: int) -> bool:
    db_campaign = db.query(models.Campaign).filter(models.Campaign.id == campaign_id).first()
    if db_campaign:
        db.delete(db_campaign)
        db.commit()
        return True
    return False


# Reference Data CRUD
def get_quest_types(db: Session) -> List[models.QuestType]:
    return db.query(models.QuestType).all()


def get_difficulties(db: Session) -> List[models.Difficulty]:
    return db.query(models.Difficulty).all()


def get_interests(db: Session) -> List[models.Interest]:
    return db.query(models.Interest).all()


def create_quest_type(db: Session, name: str) -> models.QuestType:
    db_quest_type = models.QuestType(name=name)
    db.add(db_quest_type)
    db.commit()
    db.refresh(db_quest_type)
    return db_quest_type


def create_difficulty(db: Session, name: str) -> models.Difficulty:
    db_difficulty = models.Difficulty(name=name)
    db.add(db_difficulty)
    db.commit()
    db.refresh(db_difficulty)
    return db_difficulty


def create_interest(db: Session, name: str) -> models.Interest:
    db_interest = models.Interest(name=name)
    db.add(db_interest)
    db.commit()
    db.refresh(db_interest)
    return db_interest