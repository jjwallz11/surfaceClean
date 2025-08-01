# app/schemas/faqs.py

from pydantic import BaseModel
from typing import Optional
from datetime import date

class FAQBase(BaseModel):
    question: str
    answer: str
    scheduled_post_date: Optional[date] = None

class FAQCreate(FAQBase):
    pass

class FAQUpdate(BaseModel):
    question: Optional[str] = None
    answer: Optional[str] = None

class FAQResponse(FAQBase):
    id: int

    class Config:
         model_config = {
        "from_attributes": True
    }