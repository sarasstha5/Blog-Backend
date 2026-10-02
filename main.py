from fastapi import FastAPI
from src.db.connection import Base,engine
from src.users.router import router as user_router


app = FastAPI()

Base.metadata.create_all(bind=engine)

app.include_router(user_router)

