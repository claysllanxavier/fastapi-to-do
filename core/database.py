from typing import Any, Generator

from sqlalchemy import create_engine, MetaData
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import as_declarative, declared_attr

from .config import settings

'''
Arquivo responsável pelo banco de dados

- Model principal que será herdado pelos outros models de outras app
- Cria uma instância do banco e finaliza ao finalizar a transação
'''

@as_declarative()
class Base:
    id: Any
    __name__: str
    # Generate __tablename__ automatically
    @declared_attr
    def __tablename__(cls) -> str:
        return cls.__name__.lower()


SQLALCHEMY_DATABASE_URI: str = f"{settings.db_connection}://{settings.db_username}:{settings.db_password}@{settings.db_host}:{settings.db_port}/{settings.db_database}"

engine = create_engine(SQLALCHEMY_DATABASE_URI, pool_pre_ping=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db() -> Generator:
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()