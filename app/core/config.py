import secrets
from typing import List

from pydantic import AnyHttpUrl, BaseSettings

class Settings(BaseSettings):
    API_V1_STR: str = "/api/v1"
    SECRET_KEY: str = secrets.token_urlsafe(32)
    SERVER_NAME: str = 'localhost'
    SERVER_HOST: AnyHttpUrl = 'http://localhost'
    PROJECT_NAME: str = "To-do"
    BACKEND_CORS_ORIGINS: List[AnyHttpUrl] = ['http://localhost']
    SQLALCHEMY_DATABASE_URI: str = "sqlite:///./test.db"

    class Config:
        case_sensitive = True


settings = Settings()