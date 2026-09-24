from enum import Enum
from sqlmodel import SQLModel, Field


class EventStatus(str, Enum):
    Open = "Open"
    Closed = "Closed"


class Event(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    title: str
    venue: str
    capacity: int
    organizer: str
    status: EventStatus = Field(default=EventStatus.Open)


class Reservation(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    event_id: int
    student_name: str
    roll_number: str
    email: str