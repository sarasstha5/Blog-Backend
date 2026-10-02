from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from src.posts.model import Post
from src.scheme.post import CreatePost, UpdatePost


def create_post(db: Session, data: CreatePost):
    post = Post(
        title=data.title,
        content=data.content,
    )
    db.add(post)
    db.commit()
    db.refresh(post)
    return post


def get_posts(db: Session):
    return db.query(Post).all()


def get_post(db: Session, post_id: int) -> Post:
    post = db.query(Post).filter(Post.id == post_id).first()
    if post is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Post not found",
        )
    return post


def update_post(db: Session, post_id: int, data: UpdatePost):
    post = db.query(Post).filter(Post.id == post_id).first()
    if post is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Post not found",
        )

    post.title = data.title
    post.content = data.content
    db.commit()
    db.refresh(post)
    return post


def delete_post(db: Session, post_id: int):
    post = get_post(db, post_id)
    db.delete(post)
    db.commit()