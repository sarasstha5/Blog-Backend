from fastapi import FastAPI, Depends,HTTPException
from src.db.connection import get_db 
from src.users.model import User
from sqlalchemy.orm import Session
from src.scheme.user import CreateUser, UserResponse, UserLogin
from src.auth.security import hash_password, verify_password


app = FastAPI()

#register
def register(user: CreateUser, db: Session):

    hashed_password = hash_password(user.password)
    new_user = User(
        name=user.name,
        email=user.email,
        hashed_password=hashed_password,
        is_active= True
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    db.close()

    return new_user

#login
def login(user: UserLogin,db: Session = Depends(get_db)):
    existing_user = db.query(User).filter(User.email == user.email).first()

    if not existing_user:
        raise HTTPException(
            status_code=404,
            detail="User not found"
        )

    if not verify_password(user.password, existing_user.hashed_password):
        raise HTTPException(
            status_code=401,
            detail="Incorrect password"
        )

    return {
        "message": "Login successful",
        "user_id": existing_user.id,
        "name": existing_user.name,
        "email": existing_user.email
    }