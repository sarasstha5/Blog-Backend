from src.db.connection import Base
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from src.tags.association import post_tags

class Tag(Base):
    __tablename__ = "tags"

    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True, nullable=False)
    posts = relationship("Post",secondary=post_tags,back_populates="tags")