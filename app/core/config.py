import secrets
from typing import List

from pydantic import AnyHttpUrl, BaseSettings

class Settings(BaseSettings):
    app_name: str
    api_str: str = "/api/v1"
    app_secret: str
    app_url: AnyHttpUrl
    backend_cors_origins: List[AnyHttpUrl] = ['http://localhost']

    db_connection: str
    db_host: str
    db_port: int
    db_database: str
    db_username: str
    db_password: str
    
    class Config:
        env_file = ".env"


settings = Settings()