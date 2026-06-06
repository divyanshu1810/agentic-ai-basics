# event_service/schemas.py
from pydantic import BaseModel, Field, EmailStr, field_validator, ConfigDict
from datetime import date, datetime
class EventCreate(BaseModel):
    title: str = Field(min_length=1, max_length=200)
    city: str | None = None
    date: date
    organizer: str | None = None
    organizer_email: EmailStr | None = None
    @field_validator("title")
    @classmethod
    def title_not_empty(cls, v):
        if not v.strip():
            raise ValueError("Title cannot be empty")
        return v
class EventUpdate(BaseModel):
    title: str | None = None
    city: str | None = None
    date: date
    organizer: str | None = None
    organizer_email: EmailStr | None = None
class EventOut(EventCreate):
    id: int
    class Config:
        from_attributes = True
