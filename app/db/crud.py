from sqlalchemy.orm import Session
from sqlalchemy import and_, or_
from typing import List, Optional, Tuple
from app.db import models, schemas


# User CRUD
def get_user(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()


def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()


def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.User).offset(skip).limit(limit).all()


def create_user(db: Session, user: schemas.UserCreate):
    db_user = models.User(**user.model_dump())
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


# Location CRUD
def get_location(db: Session, location_id: int):
    return db.query(models.Location).filter(models.Location.id == location_id).first()


def get_locations(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Location).offset(skip).limit(limit).all()


def create_location(db: Session, location: schemas.LocationCreate):
    db_location = models.Location(**location.model_dump())
    db.add(db_location)
    db.commit()
    db.refresh(db_location)
    return db_location


# Quest CRUD
def get_quest(db: Session, quest_id: int):
    return db.query(models.Quest).filter(models.Quest.id == quest_id).first()


def get_quests(
    db: Session, 
    skip: int = 0, 
    limit: int = 100,
    is_public: Optional[bool] = None,
    difficulty_id: Optional[int] = None,
    interest_id: Optional[int] = None
) -> Tuple[List[models.Quest], int]:
    query = db.query(models.Quest)
    
    if is_public is not None:
        query = query.filter(models.Quest.is_public == is_public)
    if difficulty_id:
        query = query.filter(models.Quest.difficulty_id == difficulty_id)
    if interest_id:
        query = query.filter(models.Quest.interest_id == interest_id)
    
    total = query.count()
    quests = query.offset(skip).limit(limit).all()
    
    return quests, total


def create_quest(db: Session, quest: schemas.QuestCreate, author_id: int):
    quest_data = quest.model_dump()
    quest_data["author_id"] = author_id
    db_quest = models.Quest(**quest_data)
    db.add(db_quest)
    db.commit()
    db.refresh(db_quest)
    return db_quest


def update_quest(db: Session, quest_id: int, quest_data: schemas.QuestUpdate):
    db_quest = db.query(models.Quest).filter(models.Quest.id == quest_id).first()
    if db_quest:
        update_data = quest_data.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_quest, field, value)
        db.commit()
        db.refresh(db_quest)
    return db_quest


def like_quest(db: Session, quest_id: int):
    db_quest = db.query(models.Quest).filter(models.Quest.id == quest_id).first()
    if db_quest:
        db_quest.likes = (db_quest.likes or 0) + 1
        db.commit()
        db.refresh(db_quest)
    return db_quest


def bookmark_quest(db: Session, quest_id: int):
    db_quest = db.query(models.Quest).filter(models.Quest.id == quest_id).first()
    if db_quest:
        db_quest.bookmarks = (db_quest.bookmarks or 0) + 1
        db.commit()
        db.refresh(db_quest)
    return db_quest


# Campaign CRUD
def get_campaign(db: Session, campaign_id: int):
    return db.query(models.Campaign).filter(models.Campaign.id == campaign_id).first()


def get_campaigns(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Campaign).offset(skip).limit(limit).all()


def create_campaign(db: Session, campaign: schemas.CampaignCreate, author_id: int):
    campaign_data = campaign.model_dump()
    campaign_data["author_id"] = author_id
    db_campaign = models.Campaign(**campaign_data)
    db.add(db_campaign)
    db.commit()
    db.refresh(db_campaign)
    return db_campaign


# Reference Data CRUD
def get_quest_types(db: Session):
    return db.query(models.QuestType).all()


def get_difficulties(db: Session):
    return db.query(models.Difficulty).all()


def get_interests(db: Session):
    return db.query(models.Interest).all()


def create_quest_type(db: Session, name: str):
    db_quest_type = models.QuestType(name=name)
    db.add(db_quest_type)
    db.commit()
    db.refresh(db_quest_type)
    return db_quest_type


def create_difficulty(db: Session, name: str):
    db_difficulty = models.Difficulty(name=name)
    db.add(db_difficulty)
    db.commit()
    db.refresh(db_difficulty)
    return db_difficulty


def create_interest(db: Session, name: str):
    db_interest = models.Interest(name=name)
    db.add(db_interest)
    db.commit()
    db.refresh(db_interest)
    return db_interest