from typing import Optional

from pydantic import BaseModel, EmailStr


# Shared properties
class UserBase(BaseModel):
  email: Optional[EmailStr] = None
  is_active: Optional[bool] = True
  is_superuser: bool = False
  first_name: Optional[str] = None
  last_name: Optional[str] = None
  username: str


# Properties to receive via API on creation
class UserCreate(UserBase):
    password: str


# Properties to receive via API on update
class UserUpdate(UserBase):
    password: Optional[str] = None


class UserInDBBase(UserBase):
    id: int

    class Config:
        orm_mode = True


# Additional properties to return via API
class User(UserInDBBase):
    pass


# Additional properties stored in DB
class UserInDB(UserInDBBase):
    password: str



class UserToken(User):
    access_token: str
    token_type: str


class TokenPayload(BaseModel):
    sub: Optional[int] = None



# Permisions
class PermissionBase(BaseModel):
  app: str
  name: str

class PermissionCreate(PermissionBase):
    pass

class PermissionUpdate(PermissionBase):
    pass

class PermissionInDBBase(PermissionBase):
    id: int

    class Config:
        orm_mode = True


# Additional properties to return via API
class Permission(PermissionInDBBase):
    pass


# Additional properties stored in DB
class PermisionInDB(PermissionInDBBase):
    pass

