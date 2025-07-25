# app/schemas/faqs.py

from pydantic import BaseModel
from typing import Optional

# Optional base (used for updates)
class FAQBase(BaseModel):
    question: Optional[str] = None
    answer: Optional[str] = None

# Required for creation
class FAQCreate(BaseModel):
    question: str
    answer: str

# Output
class FAQOut(FAQBase):
    id: int

    class Config:
        orm_mode = True