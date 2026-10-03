from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from src.catogeries.model import Category
from src.posts.model import Post
from src.scheme.post import CreatePost, UpdatePost
from src.users.model import User


def create_post(db: Session, data: CreatePost, author_id: int):
    if data.category_id is not None:
        category = db.query(Category).filter(Category.id == data.category_id).first()
        if category is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Category not found",
            )

    post = Post(
        title=data.title,
        content=data.content,
        author_id=author_id,
        category_id=data.category_id,
    )
    db.add(post)
    db.commit()
    db.refresh(post)
    return post


def get_posts(db: Session):
    return db.query(Post).all()


def get_post(db: Session, post_id: int):
    post = db.query(Post).filter(Post.id == post_id).first()
    if post is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Post not found",
        )
    return post


def update_post(db: Session, post_id: int, data: UpdatePost, user: User):
    post = db.query(Post).filter(Post.id == post_id).first()
    if post is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Post not found",
        )
    if post.author_id != user.id and user.role != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You can only update your own posts",
        )

    post.title = data.title
    post.content = data.content
    db.commit()
    db.refresh(post)
    return post


def delete_post(db: Session, post_id: int, user: User):
    post = db.query(Post).filter(Post.id == post_id).first()
    if post is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Post not found",
        )
    if post.author_id != user.id and user.role != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You can only delete your own posts",
        )
    db.delete(post)
    db.commit()