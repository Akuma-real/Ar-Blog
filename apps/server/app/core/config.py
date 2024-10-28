from pydantic_settings import BaseSettings
from typing import Optional

class Settings(BaseSettings):
    PROJECT_NAME: str = "Ar-Blog"
    VERSION: str = "0.1.0"
    API_V1_STR: str = "/api/v1"
    
    # MongoDB配置
    MONGODB_URL: str = "mongodb://localhost:27017"
    MONGODB_DB_NAME: str = "server"

    class Config:
        case_sensitive = True
        env_file = ".env"

settings = Settings()
