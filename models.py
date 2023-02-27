from uuid import uuid4
from pydantic import BaseModel, Field, validator
class Pebble(BaseModel):
    id: str | None = Field(default_factory=lambda: uuid4().hex)
    index: int

    @validator('id')
    def validate_id(cls, v: str | None):
        return uuid4().hex if not v else v