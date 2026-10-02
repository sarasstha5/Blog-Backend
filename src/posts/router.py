from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from src.db.connection import get_db
from src.posts import controller
from src.scheme.post import CreatePost, PostResponse, UpdatePost

router = APIRouter(prefix="/posts")


@router.post("/", response_model=PostResponse, status_code=status.HTTP_201_CREATED)
def create_post(data: CreatePost, db: Session = Depends(get_db)):
    return controller.create_post(db, data)


@router.get("/", response_model=list[PostResponse])
def get_posts(db: Session = Depends(get_db)):
    return controller.get_posts(db)


@router.get("/{post_id}", response_model=PostResponse)
def get_post(post_id: int, db: Session = Depends(get_db)):
    return controller.get_post(db, post_id)

@router.put("/{post_id}", response_model=PostResponse)
def update_post(post_id: int, data: UpdatePost, db: Session = Depends(get_db)):
    return controller.update_post(db, post_id, data)

@router.delete("/{post_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(post_id: int, db: Session = Depends(get_db)):
    controller.delete_post(db, post_id)