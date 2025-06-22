from pydantic import BaseModel
from typing import Optional

from .base import BaseOutputSchema


# Achievement Schemas
class AchievementBase(BaseModel):
    name: str
    description: Optional[str] = None
    icon_url: Optional[str] = None


class AchievementOut(AchievementBase, BaseOutputSchema):
    id: int