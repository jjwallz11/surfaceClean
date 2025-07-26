# app/schemas/faqs.py

from pydantic import BaseModel
from typing import Optional

class FAQBase(BaseModel):
    question: str
    answer: str

class FAQCreate(FAQBase):
    pass

class FAQUpdate(BaseModel):
    question: Optional[str] = None
    answer: Optional[str] = None

class FAQOut(FAQBase):
    id: int

    class Config:
        from_attributes = True