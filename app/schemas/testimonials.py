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

class TestimonialResponse(BaseModel):
    id: int
    author_name: str
    stars: int
    notables: Optional[str] = None
    content: Optional[str] = None

    class Config:
        model_config = {
        "from_attributes": True
    }