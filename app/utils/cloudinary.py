# app/utils/cloudinary.py

import os
import cloudinary
import cloudinary.uploader
from dotenv import load_dotenv
from fastapi import HTTPException
from typing import Union
from starlette.datastructures import UploadFile
from pathlib import Path

# Explicitly load .env from the *project root* (surfaceClean/.env)
env_path = Path(__file__).resolve().parents[1] / ".env"
load_dotenv(dotenv_path=env_path)

# Validate required environment variables early
required_envs = {
    "CLOUDINARY_CLOUD_NAME": os.getenv("CLOUDINARY_CLOUD_NAME"),
    "CLOUDINARY_API_KEY": os.getenv("CLOUDINARY_API_KEY"),
    "CLOUDINARY_API_SECRET": os.getenv("CLOUDINARY_API_SECRET"),
}

missing = [k for k, v in required_envs.items() if not v]
if missing:
    raise EnvironmentError(f"Missing required Cloudinary env vars: {', '.join(missing)}")

cloudinary.config(
    cloud_name=required_envs["CLOUDINARY_CLOUD_NAME"],
    api_key=required_envs["CLOUDINARY_API_KEY"],
    api_secret=required_envs["CLOUDINARY_API_SECRET"],
    secure=True
)

# Define allowed user emails
ALLOWED_EMAILS = {"jjparedez3@gmail.com", "surfaceclean111@yahoo.com"}

def upload_image(file: Union[str, UploadFile], current_user_email: str, folder: str = "surface_clean") -> str:
    if current_user_email not in ALLOWED_EMAILS:
        raise HTTPException(status_code=403, detail="Not authorized to upload images.")

    try:
        result = cloudinary.uploader.upload(file, folder=folder)
        return result.get("secure_url")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Cloudinary upload failed: {str(e)}")