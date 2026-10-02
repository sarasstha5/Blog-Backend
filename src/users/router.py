from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from src.scheme.user import UserResponse, CreateUser, UserLogin
from src.db.connection import get_db
from src.users import controller

router = APIRouter(prefix="/users")

@router.post("/register", response_model=UserResponse)
def register(user: CreateUser, db: Session = Depends(get_db)):
    return controller.register(user, db)

@router.post("/login")
def login(user: UserLogin, db: Session = Depends(get_db)):
    return controller.login(user, db)