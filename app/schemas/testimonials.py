# app/schemas/testimonials.py

from pydantic import BaseModel
from typing import Optional

class TestimonialBase(BaseModel):
    author_name: Optional[str] = None
    stars: Optional[int] = None
    notables: Optional[str] = None
    content: Optional[str] = None

class TestimonialCreate(BaseModel):
    author_name: str
    stars: int
    notables: Optional[str] = None
    content: Optional[str] = None

class TestimonialUpdate(TestimonialBase):
    pass

class TestimonialOut(BaseModel):
    id: int
    author_name: str
    stars: int
    notables: Optional[str] = None
    content: Optional[str] = None

    class Config:
        orm_mode = True