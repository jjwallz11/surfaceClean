# app/schemas/testimonials.py
from pydantic import BaseModel

class TestimonialBase(BaseModel):
    author: str
    content: str

class TestimonialCreate(TestimonialBase):
    pass

class TestimonialOut(TestimonialBase):
    id: int

    class Config:
        orm_mode = True