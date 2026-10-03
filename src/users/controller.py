from fastapi import FastAPI, Depends,HTTPException
from src.db.connection import get_db 
from src.users.model import User
from sqlalchemy.orm import Session
from src.scheme.user import CreateUser, UserResponse, UserLogin
from src.auth.security import hash_password, verify_password , create_access_token
from src.posts.model import Post


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

    token = create_access_token({
        "user_id": existing_user.id
    })

    return {
        "access_token": token,
        "token_type": "bearer"
    }

#admin functions
def list_users(db: Session):
    return db.query(User).order_by(User.id).all()


def delete_user(user_id: int, db: Session):
    target = db.query(User).filter(User.id == user_id).first()
    if target is None:
        raise HTTPException(status_code=404, detail="User not found")

    if target.role == "admin" and target.is_active:
        active_admin_count = (
            db.query(User)
            .filter(User.role == "admin", User.is_active.is_(True))
            .count()
        )
        if active_admin_count <= 1:
            raise HTTPException(
                status_code=409,
                detail="Cannot delete the last active admin",
            )

    has_posts = db.query(Post.id).filter(Post.author_id == user_id).first()
    if has_posts is not None:
        raise HTTPException(
            status_code=409,
            detail="Cannot delete a user who still has posts",
        )

    db.delete(target)
    db.commit()