
from .database import Base
from sqlalchemy import TIMESTAMP, Column, Integer, String, Boolean
from sqlalchemy.sql.expression import text


class Post(Base):
    __tablename__ = "posts"

    id = Column(Integer, primary_key=True, nullable=True)
    course = Column(String, nullable=False)
    teacher = Column(String, nullable=False)
    rating = Column(Integer, nullable=False)
    take_again = Column(Boolean, server_default="False", nullable=False)
    created_at = Column(TIMESTAMP(timezone=True),
                        nullable=False, server_default=text('now()'))
