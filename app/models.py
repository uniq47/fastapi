from .database import Base
from sqlalchemy import Column, Integer, String, Boolean


class Post(Base):
    __tablename__ = "posts"
    id = Column(Integer, primary_key=True, nullable=True)
    course = Column(String, nullable=False)
    teacher = Column(String, nullable=False)
    rating = Column(Integer, nullable=False)
    take_again = Column(Boolean, nullable=False)
    

