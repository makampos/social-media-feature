from fastapi import FastAPI
from backend.routers.posts import router as post_router

app = FastAPI()
app.include_router(post_router)