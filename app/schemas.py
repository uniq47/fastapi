from typing import Optional
from pydantic import BaseModel


class PostBase(BaseModel):
    course: str
    teacher: str
    rating: Optional[int] = None  # default value is none,
    take_again: Optional[bool] = None


class PostCreate(PostBase):
    pass
