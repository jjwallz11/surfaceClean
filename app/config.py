# app/config.py

from pydantic_settings import BaseSettings
from pydantic import ConfigDict
from pathlib import Path
from dotenv import load_dotenv
import os

BASE_DIR = Path(__file__).resolve().parent.parent

# Load .env first
load_dotenv(dotenv_path=BASE_DIR / ".env")

class Settings(BaseSettings):
    # === Server ===
    PORT: int = 2911
    HOST: str = "0.0.0.0"

    # === JWT Auth ===
    JWT_SECRET: str
    JWT_ALGORITHM: str = "HS256"
    JWT_EXPIRATION_MINUTES: int = 720

    # === Database ===
    DATABASE_URL: str
    SCHEMA: str = "public"

    # === Cloudinary ===
    CLOUDINARY_CLOUD_NAME: str
    CLOUDINARY_API_KEY: str
    CLOUDINARY_API_SECRET: str
    CLOUDINARY_URL: str

    model_config = ConfigDict(extra="allow")

settings = Settings()