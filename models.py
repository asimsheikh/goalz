from uuid import uuid4
from datetime import datetime
from pydantic import BaseModel, Field, validator

class FocusArea(BaseModel):
    id: str | None = Field(default_factory=lambda: uuid4().hex)
    guid: str | None = Field(default_factory=lambda: uuid4().hex)
    name: str 

    @validator('id')
    def validate_id(cls, v: str | None):
        return uuid4().hex if not v else v

    @validator('guid')
    def validate_guid(cls, v: str | None):
        return uuid4().hex if not v else v

class Task(BaseModel):
    id: str | None = Field(default_factory=lambda: uuid4().hex)
    guid: str | None = Field(default_factory=lambda: uuid4().hex)
    name: str 
    focus_area_id: str 


class Comment(BaseModel):
    id: str | None = Field(default_factory=lambda: uuid4().hex)
    date: datetime 
    text: str 

    @validator('id')
    def validate_id(cls, v: str | None):
        return uuid4().hex if not v else v