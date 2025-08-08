# app/schemas/machines.py

from pydantic import BaseModel
from typing import Optional, List
from decimal import Decimal


class MachineBase(BaseModel):
    description: Optional[str] = None
    hours_used: Optional[Decimal] = None

class MachineCreate(MachineBase):
    name: str
    price: float

class MachineUpdate(MachineBase):
    pass

class MachineResponse(BaseModel):
    id: int
    name: str
    price: float
    condition: str
    description: Optional[str] = None
    hours_used: Optional[Decimal] = None

    class Config:
        model_config = {
        "from_attributes": True
    }