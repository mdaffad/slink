from fastapi import APIRouter

from .short_link import router as short_link_router
from .user import router as user_router

api_router = APIRouter()
api_router.include_router(short_link_router, prefix="/short-links", tags=["short-link"])
api_router.include_router(user_router, prefix="/users", tags=["user"])
