from typing import Generator

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import jwt
from pydantic import ValidationError
from sqlalchemy.orm import Session
from starlette.requests import Request

from core.config import settings
from core.database import get_db
from core import security

from authentication import cruds, schemas, models

'''
Arquivo com os middlewares de segurança da app

- Neste aquivo e possível obeter o usuário logado de acordo com o token jwt
'''

reusable_oauth2 = OAuth2PasswordBearer(
  tokenUrl=f"{settings.api_str}/authentication/login"
)

def get_current_user(
    db: Session = Depends(get_db), token: str = Depends(reusable_oauth2)
) -> models.User:
    try:
        payload = jwt.decode(
            token, settings.app_secret, algorithms=[security.ALGORITHM]
        )
        token_data = schemas.TokenPayload(**payload)
    except (jwt.JWTError, ValidationError):
        raise HTTPException(
            status_code=status.HTTP_401_FORBIDDEN,
            detail="Could not validate credentials",
        )
    user = cruds.user.get(db, id=token_data.sub)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


def get_current_active_user(
    current_user: models.User = Depends(get_current_user),
) -> models.User:
    if not cruds.user.is_active(current_user):
        raise HTTPException(status_code=403, detail="Inactive user")
    return current_user


def get_current_active_superuser(
    current_user: models.User = Depends(get_current_user),
) -> models.User:
    if not cruds.user.is_superuser(current_user):
        raise HTTPException(
            status_code=403, detail="The user doesn't have enough privileges"
        )
    return current_user



def has_permission(permission_name: str) -> bool:
    def has_permission_(db: Session = Depends(get_db)):
        permission = (
            db.query(models.Permission.id).join(models.Group, models.User.groups)
                .join(models.Permission, models.Group.permissions)
                .filter(models.Permission.name == permission_name)
                .first()
        )
        if not permission:
            raise HTTPException(status_code=403, detail="You don't have permission")
        return True
    return has_permission_

