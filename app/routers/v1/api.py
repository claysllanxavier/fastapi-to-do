from fastapi import APIRouter

from app.core.config import settings
from app.routers.v1.endpoints import notes

api_router = APIRouter(prefix=settings.api_str)
api_router.include_router(notes.router, prefix="/notes", tags=["notes"])
