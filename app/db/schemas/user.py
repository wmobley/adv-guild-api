from pydantic import BaseModel, ConfigDict, EmailStr, Field
from typing import Optional
from datetime import datetime, timezone

from .base import BaseOutputSchema


class UserBase(BaseModel):
    email: EmailStr
    display_name: str
    avatar_url: Optional[str] = None
    guild_rank: Optional[str] = None

class UserCreate(UserBase):
    password: str

class UserUpdate(BaseModel):
    email: Optional[EmailStr] = None
    display_name: Optional[str] = None
    avatar_url: Optional[str] = None
    guild_rank: Optional[str] = None
    password: Optional[str] = None

class UserOut(UserBase, BaseOutputSchema):
    id: int
    is_active: bool
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: Optional[datetime] = Field(default=None)

class UserLogin(BaseModel):
    email: str

class UserResponse(BaseModel):
    user: UserOut
    access_token: str
    token_type: str = "bearer"