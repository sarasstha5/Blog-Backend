from fastapi import APIRouter, Depends, Response, status
from sqlalchemy.orm import Session

from src.auth.security import require_admin
from src.db.connection import get_db
from src.scheme.tags import TagCreate, TagResponse
from tags import controller

router = APIRouter(
    prefix="/admin/tags",
    tags=["Admin Tags"],
    dependencies=[Depends(require_admin)],
)


@router.post("/", response_model=TagResponse, status_code=status.HTTP_201_CREATED)
def create_tag(data: TagCreate, db: Session = Depends(get_db)):
    return controller.create_tag(db, data)


@router.get("/", response_model=list[TagResponse])
def get_tags(db: Session = Depends(get_db)):
    return controller.get_tags(db)


@router.get("/{tag_id}", response_model=TagResponse)
def get_tag(tag_id: int, db: Session = Depends(get_db)):
    return controller.get_tag(db, tag_id)


@router.put("/{tag_id}", response_model=TagResponse)
def update_tag(tag_id: int, data: TagCreate, db: Session = Depends(get_db)):
    return controller.update_tag(db, tag_id, data)


@router.delete("/{tag_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_tag(tag_id: int, db: Session = Depends(get_db)):
    controller.delete_tag(db, tag_id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)