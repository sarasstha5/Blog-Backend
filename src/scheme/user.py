from pydantic import BaseModel


class CreateUser(BaseModel):
    name: str
    email: str
    password: str
    is_active: bool = True


class UserLogin(BaseModel):
    email: str
    password: str


class UserResponse(BaseModel):
    id: int
    name: str
    email: str

