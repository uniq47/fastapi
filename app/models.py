from sqlalchemy import Column, Integer, String, Boolean, TIMESTAMP, text
from .database import Base


class Post(Base):
    __tablename__ = "posts"

    id = Column(Integer, primary_key=True, nullable=True)
    course = Column(String, nullable=False)
    teacher = Column(String, nullable=False)
    rating = Column(Integer, nullable=False)
    take_again = Column(Boolean, server_default="False", nullable=False)
    created_at = Column(TIMESTAMP(timezone=True),
                        nullable=False, server_default=text('now()'))


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, nullable=True)
    email = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=False)
    created_at = Column(TIMESTAMP(timezone=True),
                        nullable=False, server_default=text('now()'))
