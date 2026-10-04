from fastapi import HTTPException, status
from sqlalchemy import delete, func, select
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.orm import Session

from src.likes.association import post_likes
from src.posts.model import Post


def like_post(db: Session, post_id: int, user_id: int):
    post = db.query(Post).filter(Post.id == post_id).first()
    if post is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Post not found",
        )

    statement = (
        insert(post_likes)
        .values(user_id=user_id, post_id=post_id)
        .on_conflict_do_nothing(
            index_elements=[post_likes.c.user_id, post_likes.c.post_id]
        )
    )
    db.execute(statement)
    db.commit()

    like_count = db.execute(
        select(func.count())
        .select_from(post_likes)
        .where(post_likes.c.post_id == post_id)
    ).scalar_one()
    return {"liked": True, "like_count": like_count}


def unlike_post(db: Session, post_id: int, user_id: int):
    post = db.query(Post).filter(Post.id == post_id).first()
    if post is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Post not found",
        )

    db.execute(
        delete(post_likes).where(
            post_likes.c.post_id == post_id,
            post_likes.c.user_id == user_id,
        )
    )
    db.commit()

    like_count = db.execute(
        select(func.count())
        .select_from(post_likes)
        .where(post_likes.c.post_id == post_id)
    ).scalar_one()
    return {"liked": False, "like_count": like_count}
