from fastapi import APIRouter, Depends, Response, status
from sqlalchemy.orm import Session
from src.auth.security import require_admin
from src.scheme.user import UserResponse, CreateUser, UserLogin
from src.db.connection import get_db
from src.users import controller

router = APIRouter(prefix="/users")
admin_router = APIRouter(
    prefix="/admin/users",
    dependencies=[Depends(require_admin)],
)

@router.post("/register", response_model=UserResponse)
def register(user: CreateUser, db: Session = Depends(get_db)):
    return controller.register(user, db)

@router.post("/login")
def login(user: UserLogin, db: Session = Depends(get_db)):
    return controller.login(user, db)

#admin_router.post("/", response_model=UserResponse)
@admin_router.get("/", response_model=list[UserResponse])
def list_users(db: Session = Depends(get_db)):
    return controller.list_users(db)


@admin_router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user(user_id: int, db: Session = Depends(get_db)):
    controller.delete_user(user_id, db)
    return Response(status_code=status.HTTP_204_NO_CONTENT)