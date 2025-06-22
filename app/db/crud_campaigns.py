from sqlalchemy.orm import Session
from typing import List
from app.db.models import Campaign
from app.db.schemas import CampaignCreate, CampaignUpdate


def create_campaign(db: Session, campaign: CampaignCreate, author_id: int) -> Campaign:
    db_campaign = Campaign(**campaign.model_dump(), author_id=author_id)
    db.add(db_campaign)
    return db_campaign


def get_campaigns(db: Session, skip: int = 0, limit: int = 100) -> List[Campaign]:
    return db.query(Campaign).offset(skip).limit(limit).all()


def get_campaign(db: Session, campaign_id: int) -> Campaign | None:
    return db.query(Campaign).filter(Campaign.id == campaign_id).first()


def update_campaign(db: Session, db_campaign: Campaign, campaign_data: CampaignUpdate) -> Campaign:
    update_data = campaign_data.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_campaign, key, value)
    db.add(db_campaign)
    return db_campaign


def delete_campaign(db: Session, campaign_id: int) -> bool:
    db_campaign = get_campaign(db, campaign_id)
    if db_campaign:
        db.delete(db_campaign)
        return True
    return False