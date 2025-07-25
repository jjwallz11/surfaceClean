# app/schemas/machines.py

from pydantic import BaseModel
from typing import Optional, List
from decimal import Decimal


class MachineBase(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    price: Optional[float] = None


class MachineCreate(BaseModel):
    name: str
    price: float
    description: Optional[str] = None
    hours_used: Optional[Decimal] = None

class MachineUpdate(MachineBase):
    pass

class MachineOut(BaseModel):
    id: int
    name: str
    price: float
    description: Optional[str] = None
    hours_used: Optional[Decimal] = None
    images: Optional[List[int]] = []

    class Config:
        orm_mode = True