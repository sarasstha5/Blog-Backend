from sqlalchemy import Column, Integer, String, Text, ForeignKey, DateTime
from datetime import datetime,timezone
from sqlalchemy.orm import relationship
from src.tags.association import post_tags

from src.db.connection import Base


class Post(Base):
    __tablename__ = "posts"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)

    title = Column(String(200), nullable=False)

    content = Column(Text, nullable=False)

    author_id = Column(Integer,ForeignKey("users.id"),nullable=False)

    created_at = Column(DateTime,
    default=lambda: datetime.now(timezone.utc)
)

    updated_at = Column(DateTime,
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc)
    )

    category_id = Column(
        Integer,
        ForeignKey("categories.id", name="fk_posts_category_id_categories"),
    )
    
    image_url = Column(String, nullable=True)

    tags = relationship("Tag",secondary=post_tags,back_populates="posts")

    category = relationship("Category", back_populates="posts")

    comments = relationship(
        "Comment",
        back_populates="post",
        cascade="all, delete-orphan",
        passive_deletes=True,
    )

    bookmarks = relationship(
        "Bookmark",
        back_populates="post",
        cascade="all, delete-orphan",
        passive_deletes=True,
    )

    @property
    def tag_ids(self):
        return [tag.id for tag in self.tags]
