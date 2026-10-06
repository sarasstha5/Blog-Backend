from fastapi import APIRouter
from sqlalchemy.orm import Session
from fastapi import FastAPI,Depends
from src.db.connection import get_db
from src.auth.security import verify_token
from src.Bookmark import controller
from src.scheme.bookmark import BookmarkResponse

router = APIRouter(prefix="/bookmarks")

@router.post("/{post_id}")
def create_bookmark(post_id,db:Session = Depends(get_db), user = Depends(verify_token) ):
    return controller.create_bookmark(post_id,db,user.id)

@router.get("/", response_model=list[BookmarkResponse])
def get_my_bookmarks(db: Session = Depends(get_db),user = Depends(verify_token)):
    return controller.get_my_bookmarks(db,user.id,)

@router.delete("/{post_id}")
def delete_bookmark(
    post_id: int,
    db: Session = Depends(get_db),
    user = Depends(verify_token)):
    return controller.delete_bookmark(post_id,db,user.id)