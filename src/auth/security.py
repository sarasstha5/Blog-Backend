from fastapi import Depends, HTTPException, status
from pwdlib import PasswordHash
from datetime import datetime, timedelta, timezone
from jose import jwt
from jose.exceptions import JWTError
from fastapi.security import OAuth2PasswordBearer
from config import settings
from sqlalchemy.orm import Session
from src.db.connection import get_db
from src.users.model import User



password_hasher = PasswordHash.recommended()

def hash_password(password: str):
    return password_hasher.hash(password)

def verify_password(password: str, hashed_password: str):
    return password_hasher.verify(password, hashed_password)

# JWT Token generation and verification
SECRET_KEY = settings.SECRET_KEY
ALGORITHM = settings.ALGORITHM
ACCESS_TOKEN_EXPIRE_MINUTES = int(
    settings.ACCESS_TOKEN_EXPIRE_MINUTES
)


def create_access_token(data: dict):
    to_encode = data.copy()

    expire = datetime.now(timezone.utc) + timedelta(
        minutes=ACCESS_TOKEN_EXPIRE_MINUTES
    )

    to_encode.update({
        "exp": expire
    })

    token = jwt.encode(
        to_encode,
        SECRET_KEY,
        algorithm=ALGORITHM
    )

    return token

#verify token

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="users/login")
def verify_token(
    token: str = Depends(oauth2_scheme),db: Session = Depends(get_db),
    ):
    try:
        token_data = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token",
            headers={"WWW-Authenticate": "Bearer"},
        )

    user_id = token_data.get("user_id")
    if not isinstance(user_id, int):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication token",
            headers={"WWW-Authenticate": "Bearer"},
        )

    user = db.query(User).filter(User.id == user_id).first()
    if user is None or not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User is inactive or no longer exists",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return user

#require_admin function
def require_admin(user: User = Depends(verify_token)) -> User:
    if user.role != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Admin privileges required",
        )
    return user