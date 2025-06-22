from pydantic import BaseModel, ConfigDict
from typing import Optional
from datetime import datetime

# Assuming User schema is available for relationships
from .user import UserOut


class CampaignBase(BaseModel):
    title: str
    description: Optional[str] = None
    is_public: bool = True

class CampaignCreate(CampaignBase):
    pass

class CampaignUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    is_public: Optional[bool] = None

class CampaignOut(CampaignBase):
    id: int
    author_id: int
    created_at: datetime
    updated_at: Optional[datetime] = None
    author: Optional[UserOut] = None  # Nested user schema for response

    model_config = ConfigDict(from_attributes=True)