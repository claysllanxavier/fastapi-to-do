from fastapi import APIRouter

from .config import settings
from users.api import router as router_users

api_router = APIRouter(prefix=settings.api_str)
api_router.include_router(router_users, prefix="/users")
