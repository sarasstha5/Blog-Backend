from fastapi import APIRouter, Depends
from src.auth.security import require_admin
from src.scheme.catogeries import CategoryCreate, CategoryResponse
from sqlalchemy.orm import Session
from src.auth.security import get_db
from src.catogeries import controller

router = APIRouter(
    prefix="/admin/categories",
    tags=["Admin Categories"],
    dependencies=[Depends(require_admin)]
)


@router.post("/", response_model=CategoryResponse) 
def create_category( data: CategoryCreate, db: Session = Depends(get_db)):
    return controller.create_category(data, db)


@router.get("/catogeries", response_model=CategoryResponse) 
def get_categories( db: Session = Depends(get_db)):
    return controller.get_categories(db)


@router.put("/catogeries/{category_id}", response_model=CategoryResponse) 
def update_category( data: CategoryCreate, category_id: int, db: Session = Depends(get_db)):
    return controller.update_category(data, category_id, db)

@router.delete("/catogeries/{category_id}", response_model=CategoryResponse) 
def delete_category( category_id: int, db: Session = Depends(get_db)):
    return controller.delete_category(category_id, db)