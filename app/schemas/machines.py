from pydantic import BaseModel
from typing import Optional, List

class MachineBase(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    specifications: Optional[str] = None
    price: Optional[float] = None
    hours_used: Optional[int] = None

class MachineCreate(MachineBase):
    name: str
    price: float

class MachineUpdate(MachineBase):
    pass

class MachineOut(MachineBase):
    id: int
    images: Optional[List[int]] = []

    class Config:
        orm_mode = True