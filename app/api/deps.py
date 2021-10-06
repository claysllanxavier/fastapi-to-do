from typing import Generator

from app import crud, models, schemas
from app.core.config import settings
from app.database.session import SessionLocal

def get_db() -> Generator:
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()