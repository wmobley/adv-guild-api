from pydantic import BaseModel, ConfigDict, Field

from typing import List, Optional
from datetime import datetime, timezone


# Base class for all output schemas
class BaseOutputSchema(BaseModel):
    # Pydantic V2 uses model_config instead of class Config
    model_config = ConfigDict(from_attributes=True)


# User Schemas
class UserBase(BaseModel):
    email: Optional[str] = None
    display_name: Optional[str] = None  # Changed from username to match models.User
    avatar_url: Optional[str] = None    # Added to match models.User
    guild_rank: Optional[str] = None    # Added to match models.User
    # first_name and last_name are not in models.User, so they are removed.


class UserCreate(UserBase):
    email: str
    display_name: str  # Changed from username


class UserUpdate(BaseModel):
    email: Optional[str] = None
    display_name: Optional[str] = None  # Changed from username
    avatar_url: Optional[str] = None    # Added
    guild_rank: Optional[str] = None    # Added
    # first_name and last_name are not in models.User, so they are removed.


class UserOut(UserBase, BaseOutputSchema):
    id: int
    is_active: bool = True
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc)) # Use default_factory for datetime
    updated_at: Optional[datetime] = Field(default=None) # Added to match models.User and test data
    
    model_config = ConfigDict(from_attributes=True)



class UserLogin(BaseModel):
    email: str


class UserResponse(BaseModel):
    user: UserOut
    access_token: str
    token_type: str = "bearer"


# Location Schemas
class LocationBase(BaseModel):
    name: str
    description: Optional[str] = None
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    address: Optional[str] = None
    city: Optional[str] = None
    country: Optional[str] = None


class LocationCreate(LocationBase):
    pass


class LocationOut(LocationBase, BaseOutputSchema):
    id: int


# Reference Data Schemas
class QuestTypeBase(BaseModel):
    name: str


class QuestTypeOut(QuestTypeBase, BaseOutputSchema):
    id: int


class DifficultyBase(BaseModel):
    name: str


class DifficultyOut(DifficultyBase, BaseOutputSchema):
    id: int


class InterestBase(BaseModel):
    name: str


class InterestOut(InterestBase, BaseOutputSchema):
    id: int


# Campaign Schemas
class CampaignBase(BaseModel):
    title: str  # Changed from name to match models.Campaign and CampaignOut
    description: Optional[str] = None
    is_public: bool = True

class CampaignUpdate(BaseModel): # Don't inherit CampaignBase if you want to make formerly required fields optional
    title: Optional[str] = None
    description: Optional[str] = None
    is_public: Optional[bool] = None # Match field in CampaignBase if this is what's intended for update
    # is_active is not in CampaignBase or models.Campaign, consider removing or adding to model/Base
    
class CampaignCreate(CampaignBase):
    pass


class CampaignOut(BaseModel):
    id: int
    title: str
    description: Optional[str] = None
    author_id: int
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True) # Explicitly add config here too


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
    updated_at: Optional[datetime] = None # Should be Optional based on model? Or is onupdate always setting it? Model says nullable=True. Let's make it Optional.
    
    model_config = ConfigDict(from_attributes=True)


class QuestListResponse(BaseModel):
    quests: List[QuestOut]
    total: int
    skip: int
    limit: int


# Comment Schemas
class CommentBase(BaseModel):
    content: str
    quest_id: int


class CommentCreate(CommentBase):
    pass


class CommentOut(CommentBase, BaseOutputSchema):
    id: int
    author_id: int
    created_at: datetime
    author: Optional[UserOut] = None


# Follow Schemas
class FollowCreate(BaseModel):
    followee_id: int


class FollowOut(BaseOutputSchema):
    id: int
    follower_id: int
    followee_id: int
    created_at: datetime
    follower: Optional[UserOut] = None
    followee: Optional[UserOut] = None


# Achievement Schemas
class AchievementBase(BaseModel):
    name: str
    description: Optional[str] = None
    icon_url: Optional[str] = None


class AchievementOut(AchievementBase, BaseOutputSchema):
    id: int


# Quest Log Entry Schemas
class QuestLogEntryBase(BaseModel):
    note: str
    location_id: int


class QuestLogEntryCreate(QuestLogEntryBase):
    pass


class QuestLogEntryOut(QuestLogEntryBase, BaseOutputSchema):
    id: int
    timestamp: datetime
    location: Optional[LocationOut] = None