from fastapi import HTTPException,Depends
from src.db.connection import get_db
from src.scheme.catogeries import CategoryCreate
from sqlalchemy.orm import Session
from src.catogeries.model import Category


def create_category(data: CategoryCreate, db: Session):
    new_category = Category(name=data.name)
    db.add(new_category)
    db.commit()
    db.refresh(new_category)
    return new_category

def get_categories( db: Session = Depends(get_db)):
    return db.query(Category).all()

def update_category( data: CategoryCreate, category_id: int, db: Session = Depends(get_db)):
    category = db.query(Category).filter(Category.id == category_id).first()
    if not category:
        raise HTTPException(
            status_code=404,
            detail="Category not found"
        )
    category.name = data.name
    db.commit()
    db.refresh(category)
    return category

def delete_category( category_id: int, db: Session = Depends(get_db)):
    category = db.query(Category).filter(Category.id == category_id).first()
    if not category:
        raise HTTPException(
            status_code=404,
            detail="Category not found"
        )
    db.delete(category)
    db.commit()
    return category