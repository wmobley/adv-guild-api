from sqlalchemy.orm import Session
from typing import List
from app.db import models

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
    return db_quest_type


def create_difficulty(db: Session, name: str) -> models.Difficulty:
    db_difficulty = models.Difficulty(name=name)
    db.add(db_difficulty)
    return db_difficulty


def create_interest(db: Session, name: str) -> models.Interest:
    db_interest = models.Interest(name=name)
    db.add(db_interest)
    return db_interest