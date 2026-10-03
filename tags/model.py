from src.db.connection import Base
from sqlalchemy import Column, Integer, String

class Tag(Base):
    __tablename__ = "tags"

    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True, nullable=False)