from src.db.connection import Base
from sqlalchemy import Column, Integer, ForeignKey,UniqueConstraint
from sqlalchemy.orm import relationship

class Bookmark(Base):
    __tablename__ = "bookmarks"
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    post_id = Column(
        Integer, ForeignKey("posts.id", ondelete="CASCADE"), nullable=False
    )

    post = relationship("Post",back_populates="bookmarks")

    __table_args__ = (
        UniqueConstraint("user_id", "post_id", name="unique_user_post_bookmark"),   #restrict the duplicate user_id and post_id
    )