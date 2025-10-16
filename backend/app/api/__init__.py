from fastapi import APIRouter
from app.api import auth, stories

api_router = APIRouter()

api_router.include_router(auth.router, prefix="/auth", tags=["auth"])
api_router.include_router(stories.router, prefix="/stories", tags=["stories"])