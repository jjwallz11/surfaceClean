# app/config.py

from pydantic_settings import BaseSettings
from pydantic import ConfigDict
from pathlib import Path
from dotenv import load_dotenv
import os

BASE_DIR = Path(__file__).resolve().parent.parent

# Detect environment
ENV = os.getenv("ENVIRONMENT", "development")
ENV_FILE = BASE_DIR / f".env.{ENV}" if ENV != "development" else BASE_DIR / ".env"

# ✅ Explicitly load the .env file before Pydantic initializes
load_dotenv(dotenv_path=ENV_FILE)

class Settings(BaseSettings):
    DATABASE_URL: str
    SECRET_KEY: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 720
    ALGORITHM: str = "HS256"
    DEBUG: bool = ENV == "development"
    ENVIRONMENT: str = ENV
    SCHEMA: str = "public"
    SQLALCHEMY_ECHO: bool = DEBUG

    model_config = ConfigDict(extra="allow")  # ENV loading handled above

    @property
    def SQLALCHEMY_DATABASE_URI(self):
        return self.DATABASE_URL  # sync engine uses plain postgresql://

settings = Settings()