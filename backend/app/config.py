from pydantic_settings import BaseSettings
from typing import List
import os


class Settings(BaseSettings):
    """Application settings loaded from environment variables"""
    
    # API Keys
    gemini_api_key: str
    
    # Database
    database_url: str
    
    # Firebase (Optional for now, add when implementing auth)
    firebase_project_id: str = ""
    
    # ChromaDB
    chroma_db_path: str = "./data/chroma_db"
    
    # Backend
    backend_url: str = "http://localhost:8000"
    backend_cors_origins: List[str] = ["http://localhost:3000"]
    
    # Frontend
    frontend_url: str = "http://localhost:3000"
    
    # Environment
    environment: str = "development"
    debug: bool = True
    
    # Session
    secret_key: str = "change-this-in-production"
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 30
    
    class Config:
        env_file = ".env"
        case_sensitive = False
        extra = "ignore"


settings = Settings()
