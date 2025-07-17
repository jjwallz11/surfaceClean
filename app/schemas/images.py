# app/schemas/images.py
from pydantic import BaseModel
from typing import Optional

class ImageBase(BaseModel):
    url: str
    caption: Optional[str]

class ImageCreate(ImageBase):
    pass

class ImageOut(ImageBase):
    id: int
    machine_id: Optional[int] = None

    class Config:
        orm_mode = True