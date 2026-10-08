# src/likes/model.py

from sqlalchemy import Table, Column, Integer, ForeignKey
from src.db.connection import Base


post_likes = Table(
    "post_likes",
    Base.metadata,

    Column("user_id", Integer, ForeignKey("users.id"), primary_key=True),
    Column(
        "post_id",
        Integer,
        ForeignKey("posts.id", ondelete="CASCADE"),
        primary_key=True,
    ),
)