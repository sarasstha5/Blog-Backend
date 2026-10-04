from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from src.catogeries.model import Category
from src.posts.model import Post
from src.scheme.post import CreatePost, UpdatePost
from src.tags.model import Tag
from src.users.model import User
from  fastapi import Query

def create_post(db: Session, data: CreatePost, author_id: int):
    existing_post = db.query(Post).filter(Post.title == data.title).first()
    if existing_post is not None:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="A post with this title already exists",
        )

    if data.category_id is not None:
        category = db.query(Category).filter(Category.id == data.category_id).first()
        if category is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Category not found",
            )

    tags = db.query(Tag).filter(Tag.id.in_(data.tag_ids)).all()
    if len(tags) != len(set(data.tag_ids)):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="One or more tags not found",
        )

    post = Post(
        title=data.title,
        content=data.content,
        author_id=author_id,
        category_id=data.category_id,
    )
    post.tags = tags
    db.add(post)
    db.commit()
    db.refresh(post)
    return post

#get post
def get_posts(db: Session, page):
    limit = 10
    skip = (page - 1) * limit                             
    return db.query(Post).offset(skip).limit(limit).all()


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

    existing_post = (
        db.query(Post)
        .filter(Post.title == data.title, Post.id != post_id)
        .first()
    )
    if existing_post is not None:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="A post with this title already exists",
        )

    tags = db.query(Tag).filter(Tag.id.in_(data.tag_ids)).all()
    post.title = data.title
    post.content = data.content
    post.tags = tags
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