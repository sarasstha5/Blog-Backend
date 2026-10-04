from sqlalchemy.orm import Session
from fastapi import HTTPException, status,Depends
from src.auth.security import verify_token
from src.comment.model import Comment
from src.scheme.comments import CommentCreate, CommentUpdate


def create_comment(data: CommentCreate,db: Session, current_user):
    comment = Comment(
        content=data.content,
        post_id=data.post_id,
        user_id=current_user.id
    )

    db.add(comment)
    db.commit()
    db.refresh(comment)

    return comment

#get comment
def get_comments(post_id: int,db: Session ):
    comments = db.query(Comment).filter(
        Comment.post_id == post_id
    ).all()

    return comments

#update comment
def update_comment(comment_id: int,data: CommentUpdate,db: Session,current_user):
    comment = db.query(Comment).filter(
        Comment.id == comment_id
    ).first()

    if not comment:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Comment not found"
        )

    # Owner OR admin
    if (
        comment.user_id != current_user.id
        and current_user.role != "admin"
    ):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You are not allowed to edit this comment"
        )

    comment.content = data.content

    db.commit()
    db.refresh(comment)

    return comment

#delete comment
def delete_comment(
    comment_id: int,
    db: Session,
    current_user
):
    comment = db.query(Comment).filter(
        Comment.id == comment_id
    ).first()

    if not comment:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Comment not found"
        )

    if (
        comment.user_id != current_user.id
        and current_user.role != "admin"
    ):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You are not allowed to delete this comment"
        )

    db.delete(comment)
    db.commit()

    return {
        "message": "Comment deleted successfully"
    }