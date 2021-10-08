from typing import List, Optional, Union, Dict, Any

from sqlalchemy.orm import Session
from core.security import get_password_hash

from core.cruds import CRUDBase
from authentication.models import User
from authentication.schemas import UserCreate, UserUpdate


class CRUDUser(CRUDBase[User, UserCreate, UserUpdate]):
  def get_by_email(self, db: Session, *, email: str) -> Optional[User]:
        return db.query(User).filter(User.email == email).first()

  def create(self, db: Session, *, obj_in: UserCreate) -> User:
        db_obj = User(
            email=obj_in.email,
            password=get_password_hash(obj_in.password),
            first_name=obj_in.first_name,
            full_name=obj_in.full_name,
            is_superuser=obj_in.is_superuser,
            is_active=obj_in.active,
        )
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

  def update(
      self, db: Session, *, db_obj: User, obj_in: Union[UserUpdate, Dict[str, Any]]
  ) -> User:
      if isinstance(obj_in, dict):
          update_data = obj_in
      else:
          update_data = obj_in.dict(exclude_unset=True)
      if update_data["password"]:
          password = get_password_hash(update_data["password"])
          del update_data["password"]
          update_data["password"] = password
      return super().update(db, db_obj=db_obj, obj_in=update_data)

user = CRUDUser(User)