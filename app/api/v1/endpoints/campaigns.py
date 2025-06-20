from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.db import crud_campaigns, schemas # Changed
from app.core.security import get_current_user
from typing import List, Any, Optional, Dict  # Add Dict if needed


router = APIRouter()

@router.get("/", response_model=List[schemas.CampaignOut])
def get_campaigns(
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1, le=100),
    db: Session = Depends(get_db)
) -> List[schemas.CampaignOut]:
    campaigns = crud_campaigns.get_campaigns(db, skip=skip, limit=limit) # Changed
    
    # Debug: Print the first campaign to see its structure
    if campaigns:
        print(f"Campaign data: {campaigns[0].__dict__}")
    
    return [schemas.CampaignOut.model_validate(campaign) for campaign in campaigns]

@router.get("/{campaign_id}", response_model=schemas.CampaignOut)
def get_campaign(campaign_id: int, db: Session = Depends(get_db)) -> schemas.CampaignOut:
    campaign = crud_campaigns.get_campaign(db, campaign_id=campaign_id) # Changed
    if not campaign:
        raise HTTPException(status_code=404, detail="Campaign not found")
    return schemas.CampaignOut.model_validate(campaign)

@router.post("/", response_model=schemas.CampaignOut)
def create_campaign(
    campaign_data: schemas.CampaignCreate,
    current_user: schemas.UserOut = Depends(get_current_user),
    db: Session = Depends(get_db)
) -> schemas.CampaignOut:
    campaign = crud_campaigns.create_campaign(db, campaign_data, author_id=current_user.id) # Changed
    return schemas.CampaignOut.model_validate(campaign)

@router.put("/{campaign_id}", response_model=schemas.CampaignOut)
def update_campaign(
    campaign_id: int,
    campaign_data: schemas.CampaignUpdate,
    current_user: schemas.UserOut = Depends(get_current_user),
    db: Session = Depends(get_db)
) -> schemas.CampaignOut:
    # First check if campaign exists
    existing_campaign = crud_campaigns.get_campaign(db, campaign_id=campaign_id) # Changed
    if not existing_campaign:
        raise HTTPException(status_code=404, detail="Campaign not found")
    
    # Check if user is the author (authorization check)
    if existing_campaign.author_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized to update this campaign")
    campaign = crud_campaigns.update_campaign(db, db_campaign=existing_campaign, campaign_data=campaign_data)
    return schemas.CampaignOut.model_validate(campaign)

@router.delete("/{campaign_id}")
def delete_campaign(
    campaign_id: int,
    current_user: schemas.UserOut = Depends(get_current_user),
    db: Session = Depends(get_db)
) -> dict:
    # First check if campaign exists
    existing_campaign = crud_campaigns.get_campaign(db, campaign_id=campaign_id) # Changed
    if not existing_campaign:
        raise HTTPException(status_code=404, detail="Campaign not found")
    
    # Check if user is the author (authorization check)
    if existing_campaign.author_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized to delete this campaign")
    success = crud_campaigns.delete_campaign(db, campaign_id=campaign_id) # Changed
    if not success:
        raise HTTPException(status_code=404, detail="Campaign not found")
    return {"message": "Campaign deleted successfully"}