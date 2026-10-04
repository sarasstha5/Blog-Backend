from fastapi import FastAPI
from src.db.connection import Base,engine
from src.users.router import admin_router, router as user_router
from src.posts.router import router as post_router
from src.catogeries.router import router as category_router
from src.tags.router import router as tag_router


app = FastAPI()

Base.metadata.create_all(bind=engine)

app.include_router(post_router)
app.include_router(user_router)
app.include_router(admin_router)
app.include_router(category_router)
app.include_router(tag_router)
