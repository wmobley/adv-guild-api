from pydantic import BaseModel, ConfigDict


# Base class for all output schemas
class BaseOutputSchema(BaseModel):
    # Pydantic V2 uses model_config instead of class Config
    model_config = ConfigDict(from_attributes=True)