from fastapi import APIRouter

from .config import settings
from authentication.api import router as router_users

'''
Arquivos com os endpoints principais do projeto

- Deve ser importado nesse arquivo, os arquivo routers de todas as apps
'''

api_router = APIRouter(prefix=settings.api_str)
api_router.include_router(router_users, prefix="/authentication")
