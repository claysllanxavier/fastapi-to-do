from sqlalchemy import create_engine, MetaData
from sqlalchemy.orm import sessionmaker

from app.core.config import settings

metadata = MetaData()

SQLALCHEMY_DATABASE_URI: str = f"{settings.db_connection}://{settings.db_username}:{settings.db_password}@{settings.db_host}:{settings.db_port}/{settings.db_database}"

engine = create_engine(SQLALCHEMY_DATABASE_URI, pool_pre_ping=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)