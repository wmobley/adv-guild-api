from pydantic import BaseModel

from .base import BaseOutputSchema


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