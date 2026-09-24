from pydantic import BaseModel, Field
from .models import ItemStatus


class ItemCreate(BaseModel):
    title: str = Field(min_length=1)
    description: str = Field(min_length=3)
    category: str = Field(min_length=1)
    location: str = Field(min_length=1)
    reported_by: str = Field(min_length=1)
    status: ItemStatus = ItemStatus.Lost