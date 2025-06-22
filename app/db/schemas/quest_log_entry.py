from pydantic import BaseModel
from typing import Optional
from datetime import datetime

from .base import BaseOutputSchema
from .location import LocationOut


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