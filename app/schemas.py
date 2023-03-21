from typing import Optional
from pydantic import BaseModel
from datetime import datetime


class PostBase(BaseModel):
    course: str
    teacher: str
    rating: Optional[int] = None  # default value is none,
    take_again: Optional[bool] = None


class PostCreate(PostBase):
    pass


class Post(PostBase):
    id: int
    created_at: datetime

    class Config:
        orm_mode = True
