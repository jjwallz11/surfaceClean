# app/schemas/images.py

from pydantic import BaseModel
from typing import Optional

class ImageBase(BaseModel):
    url: str
    description: Optional[str] = None
    machine_id: Optional[int] = None

class ImageCreate(ImageBase):
    pass

class ImageUpdate(BaseModel):
    url: Optional[str] = None
    description: Optional[str] = None
    machine_id: Optional[int] = None

class ImageResponse(ImageBase):
    id: int

    class Config:
        model_config = {
            "from_attributes": True
        }