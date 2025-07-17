# app/schemas/faq.py
from pydantic import BaseModel

class FAQBase(BaseModel):
    question: str
    answer: str

class FAQCreate(FAQBase):
    pass

class FAQOut(FAQBase):
    id: int

    class Config:
        orm_mode = True