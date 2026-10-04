from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from src.db.connection import get_db
from src.auth.security import verify_token
from src.scheme.comments import (CommentCreate,CommentUpdate,CommentResponse)
from src.comment import controller


router = APIRouter(
    prefix="/comments",
    tags=["Comments"]
)

@router.post("/",response_model=CommentResponse)
def create(data: CommentCreate,db: Session = Depends(get_db),current_user=Depends(verify_token)):
    return controller.create_comment(data,db,current_user)

@router.post("/post/{post_id}",response_model=CommentResponse)
def create(data: CommentCreate,post_id,db: Session = Depends(get_db)):
    return controller.get_comment(post_id,db,)

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
