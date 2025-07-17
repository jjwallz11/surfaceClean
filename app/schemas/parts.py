# app/schemas/parts.py
from pydantic import BaseModel
from typing import Optional

class PartBase(BaseModel):
    name: str
    description: Optional[str]
    price: float

class PartCreate(PartBase):
    pass

class PartOut(PartBase):
    id: int

    class Config:
        orm_mode = True