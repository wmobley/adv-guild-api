from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List
from app.db.database import get_db
from app.db import crud, schemas
from app.core.security import get_current_user

router = APIRouter()


@router.get("/", response_model=List[schemas.CampaignOut])
def get_campaigns(
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1, le=100),
    db: Session = Depends(get_db)
):
    return crud.get_campaigns(db, skip=skip, limit=limit)


@router.post("/", response_model=schemas.CampaignOut)
def create_campaign(
    campaign_data: schemas.CampaignCreate,
    current_user: schemas.UserOut = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    return crud.create_campaign(db=db, campaign=campaign_data, author_id=current_user.id)


@router.get("/{campaign_id}", response_model=schemas.CampaignOut)
def get_campaign(campaign_id: int, db: Session = Depends(get_db)):
    campaign = crud.get_campaign(db, campaign_id=campaign_id)
    if not campaign:
        raise HTTPException(status_code=404, detail="Campaign not found")
    return campaign