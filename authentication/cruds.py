from typing import List, Optional, Union, Dict, Any

from sqlalchemy.orm import Session
from fastapi.encoders import jsonable_encoder
from core.security import get_password_hash, verify_password

from core.cruds import CRUDBase
from authentication.models import User, Permission, Group
from authentication.schemas import UserCreate, UserUpdate, PermissionCreate, PermissionUpdate, GroupCreate, GroupUpdate


class CRUDUser(CRUDBase[User, UserCreate, UserUpdate]):
    def get_by_email(self, db: Session, *, email: str) -> Optional[User]:
            return db.query(User).filter(User.email == email).first()

    def create(self, db: Session, *, obj_in: UserCreate) -> User:
            db_obj = User(
                email=obj_in.email,
                password=get_password_hash(obj_in.password),
                first_name=obj_in.first_name,
                last_name=obj_in.last_name,
                is_superuser=obj_in.is_superuser,
                is_active=obj_in.is_active,
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
        if 'password' in update_data:
            password = get_password_hash(update_data["password"])
            del update_data["password"]
            update_data["password"] = password
        return super().update(db, db_obj=db_obj, obj_in=update_data)

    def authenticate(self, db: Session, *, email: str, password: str) -> Optional[User]:
        user = self.get_by_email(db, email=email)
        if not user:
            return None
        if not verify_password(password, user.password):
            return None
        return user
    
    def is_active(self, user: User) -> bool:
        return user.is_active

    def is_superuser(self, user: User) -> bool:
        return user.is_superuser


user = CRUDUser(User)

class CRUDPermission(CRUDBase[Permission, PermissionCreate, PermissionUpdate]):
    pass

permission = CRUDPermission(Permission)


class CRUDGroup(CRUDBase[Group, GroupCreate, GroupUpdate]):
    def create(self, db: Session, *, obj_in: GroupCreate) -> Group:
            db_obj = Group(
                name=obj_in.name,
            )
            permissions = db.query(Permission).filter(Permission.name.in_(obj_in.permissions)).all()
            db_obj.permissions = permissions
            db.add(db_obj)
            db.commit()
            db.refresh(db_obj)
            return db_obj

    def update(
        self, db: Session, *, db_obj: Group, obj_in: GroupUpdate
    ) -> Group:
        obj_data = jsonable_encoder(db_obj)
        if isinstance(obj_in, dict):
            update_data = obj_in
        else:
            update_data = obj_in.dict(exclude_unset=True)
        for field in obj_data:
            if field in update_data:
                setattr(db_obj, field, update_data[field])
        db_obj.permissions.clear()
        permissions = db.query(Permission).filter(Permission.name.in_(obj_in.permissions)).all()
        db_obj.permissions = permissions
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj


group = CRUDGroup(Group)