# app/schemas/machines.py
from pydantic import BaseModel
from typing import Optional, List

class MachineBase(BaseModel):
    name: str
    description: Optional[str]
    specifications: Optional[str]
    price: float
    hours_used: Optional[int]

class MachineCreate(MachineBase):
    pass

class MachineOut(MachineBase):
    id: int
    images: Optional[List[int]] = []

    class Config:
        orm_mode = True