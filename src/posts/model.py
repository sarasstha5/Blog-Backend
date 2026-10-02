from sqlalchemy import Column, Integer, String, Text, ForeignKey, DateTime
from datetime import datetime,timezone

from src.db.connection import Base


class Post(Base):
    __tablename__ = "posts"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)

    title = Column(String(200), nullable=False)

    content = Column(Text, nullable=False)

    author_id = Column(
        Integer,
        ForeignKey("users.id"),
        nullable=False
    )

    created_at = Column(DateTime,default=datetime.now(timezone.utc))

    updated_at = Column(
        DateTime,
        default=datetime.now(timezone.utc),
        onupdate=datetime.now(timezone.utc)
    )