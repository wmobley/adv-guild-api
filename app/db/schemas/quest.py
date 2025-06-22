from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

from .base import BaseOutputSchema
from .user import UserOut
from .location import LocationOut
from .reference import InterestOut, DifficultyOut, QuestTypeOut
from .campaign import CampaignOut


# Quest Schemas
class QuestBase(BaseModel):
    name: str
    synopsis: str
    start_location_id: int
    destination_id: Optional[int] = None
    interest_id: int
    itinerary: str
    difficulty_id: int
    is_public: bool = True
    quest_type_id: int
    tags: Optional[str] = None
    quest_giver: Optional[str] = None
    reward: Optional[str] = None
    companions: Optional[str] = None
    lore_excerpt: Optional[str] = None
    artifacts_discovered: Optional[str] = None
    completed: bool = False
    media_urls: Optional[List[str]] = None
    campaign_id: Optional[int] = None


class QuestCreate(QuestBase):
    pass


class QuestUpdate(BaseModel):
    name: Optional[str] = None
    synopsis: Optional[str] = None
    start_location_id: Optional[int] = None
    destination_id: Optional[int] = None
    interest_id: Optional[int] = None
    itinerary: Optional[str] = None
    difficulty_id: Optional[int] = None
    is_public: Optional[bool] = None
    quest_type_id: Optional[int] = None
    tags: Optional[str] = None
    quest_giver: Optional[str] = None
    reward: Optional[str] = None
    companions: Optional[str] = None
    lore_excerpt: Optional[str] = None
    artifacts_discovered: Optional[str] = None
    completed: Optional[bool] = None
    media_urls: Optional[List[str]] = None
    campaign_id: Optional[int] = None


class QuestOut(QuestBase, BaseOutputSchema):
    id: int
    author_id: int
    created_at: datetime
    updated_at: Optional[datetime] = None
    author: Optional[UserOut] = None
    start_location: Optional[LocationOut] = None
    destination: Optional[LocationOut] = None
    interest: Optional[InterestOut] = None
    difficulty: Optional[DifficultyOut] = None
    quest_type: Optional[QuestTypeOut] = None
    campaign: Optional[CampaignOut] = None


class QuestListResponse(BaseModel):
    quests: List[QuestOut]
    total: int
    skip: int
    limit: int