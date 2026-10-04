
from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy.orm import relationship
from src.db.connection import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String(100), nullable=False)
    email = Column(String(255), unique=True, index=True, nullable=False)
    hashed_password = Column(String(255), nullable=False)
    is_active = Column(Boolean, default=True)
    role = Column(String(20), default="user", nullable=False, server_default="user")
    comments = relationship("Comment", back_populates="user")
