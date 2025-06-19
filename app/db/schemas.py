from pydantic import BaseModel, ConfigDict
from typing import Optional, List
from datetime import datetime


# User Schemas
class UserBase(BaseModel):
    display_name: str
    email: Optional[str] = None
    avatar_url: Optional[str] = None
    guild_rank: Optional[str] = None


class UserCreate(UserBase):
    pass


class UserUpdate(BaseModel):
    display_name: Optional[str] = None
    email: Optional[str] = None
    avatar_url: Optional[str] = None
    guild_rank: Optional[str] = None


class UserOut(UserBase):
    id: int
    created_at: datetime
    model_config = ConfigDict(from_attributes=True)


class UserLogin(BaseModel):
    email: str


class UserResponse(BaseModel):
    user: UserOut
    access_token: str
    token_type: str = "bearer"


# Location Schemas
class LocationBase(BaseModel):
    latitude: float
    longitude: float
    name: Optional[str] = None
    real_world_inspiration: Optional[str] = None
    description: Optional[str] = None


class LocationCreate(LocationBase):
    pass


class LocationOut(LocationBase):
    id: int
    model_config = ConfigDict(from_attributes=True)


# Reference Data Schemas
class QuestTypeBase(BaseModel):
    name: str


class QuestTypeOut(QuestTypeBase):
    id: int
    model_config = ConfigDict(from_attributes=True)


class DifficultyBase(BaseModel):
    name: str


class DifficultyOut(DifficultyBase):
    id: int
    model_config = ConfigDict(from_attributes=True)


class InterestBase(BaseModel):
    name: str


class InterestOut(InterestBase):
    id: int
    model_config = ConfigDict(from_attributes=True)


# Campaign Schemas
class CampaignBase(BaseModel):
    title: str
    description: Optional[str] = None


class CampaignCreate(CampaignBase):
    pass


class CampaignOut(CampaignBase):
    id: int
    author_id: int
    created_at: datetime
    author: Optional[UserOut] = None
    model_config = ConfigDict(from_attributes=True)


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


class QuestOut(QuestBase):
    id: int
    created_at: datetime
    updated_at: datetime
    author_id: Optional[int] = None
    likes: int = 0
    bookmarks: int = 0
    author: Optional[UserOut] = None
    start_location: Optional[LocationOut] = None
    destination: Optional[LocationOut] = None
    interest: Optional[InterestOut] = None
    difficulty: Optional[DifficultyOut] = None
    quest_type: Optional[QuestTypeOut] = None
    campaign: Optional[CampaignOut] = None
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


class CommentOut(CommentBase):
    id: int
    author_id: int
    created_at: datetime
    author: Optional[UserOut] = None
    model_config = ConfigDict(from_attributes=True)


# Follow Schemas
class FollowCreate(BaseModel):
    followee_id: int


class FollowOut(BaseModel):
    id: int
    follower_id: int
    followee_id: int
    created_at: datetime
    follower: Optional[UserOut] = None
    followee: Optional[UserOut] = None
    model_config = ConfigDict(from_attributes=True)


# Achievement Schemas
class AchievementBase(BaseModel):
    name: str
    description: Optional[str] = None
    icon_url: Optional[str] = None


class AchievementOut(AchievementBase):
    id: int
    model_config = ConfigDict(from_attributes=True)


# Quest Log Entry Schemas
class QuestLogEntryBase(BaseModel):
    note: str
    location_id: int


class QuestLogEntryCreate(QuestLogEntryBase):
    pass


class QuestLogEntryOut(QuestLogEntryBase):
    id: int
    timestamp: datetime
    location: Optional[LocationOut] = None
    model_config = ConfigDict(from_attributes=True)