from pydantic import BaseModel
from typing import Optional
from datetime import datetime

from .base import BaseOutputSchema
from .user import UserOut


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