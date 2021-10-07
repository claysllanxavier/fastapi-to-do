from typing import Any, List

from fastapi import APIRouter, Body, Depends, HTTPException
from sqlalchemy.orm import Session

from core.config import settings
from core.database import get_db

from users import schemas, cruds


router_user = APIRouter(
    prefix="/user"
)


@router_user.get("/", response_model=List[schemas.User], tags=["user"])
def read_users(
    db: Session = Depends(get_db),
    skip: int = 0,
    limit: int = 25
) -> Any:
    """
    Retrieve users.
    """
    users = cruds.user.get_multi(db, skip=skip, limit=limit)
    return users


@router_user.post("/", response_model=schemas.User, tags=["user"])
def create_user(
    *,
    db: Session = Depends(get_db),
    user_in: schemas.UserCreate
) -> Any:
    """
    Create new user.
    """
    user = cruds.user.get_by_email(db, email=user_in.email)
    if user:
        raise HTTPException(
            status_code=400,
            detail="The user with this username already exists in the system.",
        )
    user = cruds.user.create(db, obj_in=user_in)
    return user


@router_user.get("/{user_id}", response_model=schemas.User, tags=["user"])
def read_user_by_id(
    user_id: int,
    db: Session = Depends(get_db),
) -> Any:
    """
    Get a specific user by id.
    """
    user = cruds.user.get(db, id=user_id)
    if not user:
      raise HTTPException(
          status_code=404,
          detail="The user with this username does not exist in the system",
      )
    return user


@router_user.put("/{user_id}", response_model=schemas.User, tags=["user"])
def update_user(
    *,
    db: Session = Depends(get_db),
    user_id: int,
    user_in: schemas.UserUpdate
) -> Any:
    """
    Update a user.
    """
    user = cruds.user.get(db, id=user_id)
    if not user:
        raise HTTPException(
            status_code=404,
            detail="The user with this username does not exist in the system",
        )
    user = cruds.user.update(db, db_obj=user, obj_in=user_in)
    return user

@router_user.delete("/{id}", response_model=schemas.User, tags=["user"])
def delete_note(
    *,
    db: Session = Depends(get_db),
    id: int
) -> Any:
    """
    Delete an note.
    """
    user = cruds.user.get(db=db, id=id)
    if not user:
      raise HTTPException(
        status_code=404,
        detail="The user with this username does not exist in the system",
      )
    user = cruds.user.remove(db=db, id=id)
    return user


router = APIRouter()
router.include_router(router_user)