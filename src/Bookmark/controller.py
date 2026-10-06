from sqlalchemy.orm import Session
from fastapi import HTTPException,status
from src.posts.model import Post
from src.Bookmark.model import Bookmark
from src.scheme.bookmark import BookmarkResponse



def create_bookmark(post_id,db:Session,user):
    post = db.query(Post).filter(Post.id == post_id).all()
    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Post not found"
        )

    existing_bookmark = db.query(Bookmark).filter(Bookmark.user_id == user, Bookmark.post_id == post_id)
    if not existing_bookmark:
        raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Bookmark exist!"
            )

    bookmark = Bookmark(
        user_id = user,
        post_id = post_id
    )

    db.add(bookmark)
    db.commit()
    db.refresh(bookmark)

    return{
        "message": "Post bookmarked successfully",
        "bookmark": bookmark
    }


def get_my_bookmarks(db: Session,user_id:int):
    bookmarks = db.query(Bookmark).filter(
        Bookmark.user_id == user_id).all()

    return [
        BookmarkResponse(
            id=bookmark.id,
            post_id=bookmark.post_id,
            title=bookmark.post.title,
            created_at=bookmark.post.created_at
        )
        for bookmark in bookmarks
    ]



def delete_bookmark(
    post_id: int,
    db: Session,
    user_id:int
):
    bookmark = db.query(Bookmark).filter(
        Bookmark.post_id == post_id,
        Bookmark.user_id == user_id
    ).first()

    if not bookmark:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Bookmark not found"
        )

    db.delete(bookmark)
    db.commit()

    return {
        "message": "Bookmark removed successfully"
    }