# models/testimonials.py

from sqlalchemy import Column, Integer, String, Text
from app.db import Base

class Testimonial(Base):
    __tablename__ = "testimonials"

    id = Column(Integer, primary_key=True, index=True)
    author_name = Column(String, nullable=False)
    stars = Column(Integer, nullable=False)
    notables = Column(Text)  # Comma-separated values
    content = Column(Text)