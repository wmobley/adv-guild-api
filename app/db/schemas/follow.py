from pydantic import BaseModel
from typing import Optional
from datetime import datetime

from .base import BaseOutputSchema
from .user import UserOut


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