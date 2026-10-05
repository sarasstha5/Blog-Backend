from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from src.db.connection import Base


class Category(Base):
    __tablename__ = "categories"

    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True, nullable=False)
    posts = relationship("Post", back_populates="category")