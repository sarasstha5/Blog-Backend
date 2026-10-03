from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from src.scheme.tags import TagCreate
from tags.model import Tag


def create_tag(db: Session, data: TagCreate):
    existing_tag = db.query(Tag).filter(Tag.name == data.name).first()
    if existing_tag is not None:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="A tag with this name already exists",
        )

    tag = Tag(name=data.name)
    db.add(tag)
    db.commit()
    db.refresh(tag)
    return tag


def get_tags(db: Session):
    return db.query(Tag).all()


def get_tag(db: Session, tag_id: int):
    tag = db.query(Tag).filter(Tag.id == tag_id).first()
    if tag is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Tag not found",
        )
    return tag


def update_tag(db: Session, tag_id: int, data: TagCreate):
    tag = get_tag(db, tag_id)
    existing_tag = (
        db.query(Tag)
        .filter(Tag.name == data.name, Tag.id != tag_id)
        .first()
    )
    if existing_tag is not None:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="A tag with this name already exists",
        )

    tag.name = data.name
    db.commit()
    db.refresh(tag)
    return tag


def delete_tag(db: Session, tag_id: int):
    tag = get_tag(db, tag_id)
    db.delete(tag)
    db.commit()