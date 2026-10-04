from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from src.auth.security import verify_token
from src.db.connection import get_db
from src.likes import controller
from src.scheme.likes import LikeResponse
from src.users.model import User


router = APIRouter(prefix="/posts", tags=["Likes"])


@router.post("/{post_id}/like", response_model=LikeResponse)
def like_post(
    post_id: int,
    db: Session = Depends(get_db),
    user: User = Depends(verify_token),
):
    return controller.like_post(db, post_id, user.id)


@router.delete("/{post_id}/like", response_model=LikeResponse)
def unlike_post(
    post_id: int,
    db: Session = Depends(get_db),
    user: User = Depends(verify_token),
):
    return controller.unlike_post(db, post_id, user.id)
