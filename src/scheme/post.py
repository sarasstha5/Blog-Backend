from datetime import datetime

from pydantic import BaseModel


class CreatePost(BaseModel):
    title: str
    content: str
    category_id: int | None = None
    tag_ids: list[int]


class UpdatePost(BaseModel):
    title: str
    content: str
    tag_ids: list[int]


class PostResponse(BaseModel):
    id: int
    title: str
    content: str
    author_id: int
    category_id: int | None
    tag_ids: list[int]
    views: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True