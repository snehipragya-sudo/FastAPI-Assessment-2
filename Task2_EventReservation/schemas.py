from pydantic import BaseModel, Field, EmailStr
from .models import EventStatus


class EventCreate(BaseModel):
    title: str = Field(min_length=1)
    venue: str = Field(min_length=1)
    capacity: int = Field(gt=0)
    organizer: str = Field(min_length=1)
    status: EventStatus = EventStatus.Open


class ReservationCreate(BaseModel):
    student_name: str = Field(min_length=1)
    roll_number: str = Field(min_length=1)
    email: EmailStr