from uuid import uuid4
from datetime import datetime
from pydantic import BaseModel, Field, validator
class Comment(BaseModel):
    id: str | None = Field(default_factory=lambda: uuid4().hex)
    date: datetime 
    text: str 

    @validator('id')
    def validate_id(cls, v: str | None):
        return uuid4().hex if not v else v