from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from src.db.connection import get_db
from src.auth.security import verify_token
from src.scheme.comments import (CommentCreate,CommentUpdate,CommentResponse)
from src.comment import controller


router = APIRouter(
    prefix="/comments",
    tags=["Comments"]
)

@router.post("/", response_model=CommentResponse)
def create(data: CommentCreate,db: Session = Depends(get_db),current_user=Depends(verify_token)):
    return controller.create_comment(data,db,current_user)


@router.get("/post/{post_id}", response_model=list[CommentResponse])
def get_comments(
    post_id: int,
    page: int = Query(1, ge=1),
    db: Session = Depends(get_db),
):
    return controller.get_comments(post_id, page, db)

@router.put(
    "/{comment_id}",
    response_model=CommentResponse
)
def update(
    comment_id: int,
    data: CommentUpdate,
    db: Session = Depends(get_db),
    current_user=Depends(verify_token)
):
    return controller.update_comment(
        comment_id,
        data,
        db,
        current_user
    )

@router.delete("/{comment_id}")
def delete(
    comment_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(verify_token)
):
    return controller.delete_comment(
        comment_id,
        db,
        current_user
    )
