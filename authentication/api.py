from typing import Any, List

from fastapi import APIRouter, Body, Depends, HTTPException
from fastapi.encoders import jsonable_encoder
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from pydantic.networks import EmailStr

from core.database import get_db
from core.security import create_access_token

from authentication import schemas, cruds, security


router_user = APIRouter(
    prefix="/users",
    tags=['users']
)


@router_user.get("/", response_model=List[schemas.User])
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


@router_user.post("/", response_model=schemas.User)
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
            status_code=403,
            detail="The user with this username already exists in the system.",
        )
    user = cruds.user.create(db, obj_in=user_in)
    return user


@router_user.get("/{user_id}", response_model=schemas.User)
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


@router_user.put("/{user_id}", response_model=schemas.User)
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

@router_user.delete("/{id}", response_model=schemas.User)
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


router_auth = APIRouter(
     tags=['auth']
)

@router_auth.post("/login", response_model=schemas.UserToken)
def login_access_token(
    db: Session = Depends(get_db), 
    form_data: OAuth2PasswordRequestForm = Depends()
) -> Any:
    """
    OAuth2 compatible token login, get an access token for future requests
    """
    user = cruds.user.authenticate(
        db, email=form_data.username, password=form_data.password
    )
    if not user:
        raise HTTPException(status_code=403, detail="Incorrect email or password")
    elif not cruds.user.is_active(user):
        raise HTTPException(status_code=403, detail="Inactive user")
    return {
        **user.__dict__,
        "access_token": create_access_token(
            user.id
        ),
        "token_type": "bearer",
    }

@router_auth.get("/profile", response_model=schemas.User)
def read_user_me(
    db: Session = Depends(get_db),
    current_user: schemas.User = Depends(security.get_current_active_user),
) -> Any:
    """
    Get current user.
    """
    return current_user


@router_auth.put("/profile", response_model=schemas.User)
def update_user_me(
    *,
    db: Session = Depends(get_db),
    first_name: str = Body(None),
    last_name: str = Body(None),
    email: EmailStr = Body(None),
    current_user: schemas.User = Depends(security.get_current_active_user),
) -> Any:
    """
    Update own user.
    """
    current_user_data = jsonable_encoder(current_user)
    user_in = schemas.UserUpdate(**current_user_data)
    if first_name is not None:
        user_in.first_name = first_name
    if last_name is not None:
        user_in.last_name = last_name
    if email is not None:
        user_in.email = email
    user = cruds.user.update(db, db_obj=current_user, obj_in=user_in)
    return user

router = APIRouter()
router.include_router(router_user)
router.include_router(router_auth)