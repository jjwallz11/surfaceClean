# app/schemas/images.py

from pydantic import BaseModel, model_validator
from typing import Optional

class ImageBase(BaseModel):
    url: str
    description: Optional[str] = None
    machine_id: Optional[int] = None
    part_id: Optional[int] = None

class ImageCreate(ImageBase):
    @model_validator(mode="after")
    def check_machine_or_part(self) -> "ImageCreate":
        if bool(self.machine_id) == bool(self.part_id):
            raise ValueError("Exactly one of machine_id or part_id must be provided.")
        return self

class ImageOut(ImageBase):
    id: int

    class Config:
        orm_mode = True