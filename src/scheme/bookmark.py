# src/scheme/bookmark.py

from datetime import datetime
from pydantic import BaseModel


class BookmarkResponse(BaseModel):
    id: int
    post_id: int
    title: str
    created_at: datetime