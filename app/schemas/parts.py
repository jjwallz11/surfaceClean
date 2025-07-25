# app/schemas/parts.py

from pydantic import BaseModel
from typing import Optional
from decimal import Decimal

class PartBase(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    price: Optional[Decimal] = None
    quantity: Optional[int] = None

class PartCreate(BaseModel):
    name: str
    price: Decimal
    description: Optional[str] = None
    quantity: int

class PartUpdate(PartBase):
    pass

class PartOut(BaseModel):
    id: int
    name: str
    price: Decimal
    description: Optional[str] = None
    quantity: int

    class Config:
        orm_mode = True