from sqlalchemy import create_engine, MetaData
from sqlalchemy.orm import sessionmaker

from app.core.config import settings

metadata = MetaData()

engine = create_engine(settings.SQLALCHEMY_DATABASE_URI)
SessionLocal = sessionmaker(autocommit=True, bind=engine)

metadata.create_all(engine)