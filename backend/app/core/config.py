"""
Application configuration settings.
"""
import os
from pathlib import Path
from pydantic_settings import BaseSettings
from functools import lru_cache
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""
    
    # API Settings
    app_name: str = "Resume Tailoring API"
    debug: bool = False
    
    # Gemini API
    gemini_api_key: str = ""
    gemini_model: str = "gemini-2.5-flash"
    
    # File paths - base_dir is the backend folder
    base_dir: Path = Path(__file__).resolve().parent.parent.parent
    templates_dir: Path = base_dir / "templates"
    uploads_dir: Path = base_dir / "uploads"
    output_dir: Path = base_dir / "output"
    
    # CORS
    cors_origins: list[str] = ["http://localhost:3000", "http://localhost:5173"]
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


@lru_cache()
def get_settings() -> Settings:
    """Get cached settings instance."""
    return Settings()
