from datetime import datetime

from pydantic import BaseModel


class CreatePost(BaseModel):
    title: str
    content: str


class UpdatePost(BaseModel):
    title: str
    content: str


class PostResponse(BaseModel):
    id: int
    title: str
    content: str
    author_id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True