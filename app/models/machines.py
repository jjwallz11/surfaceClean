# app/models/machines.py

from sqlalchemy import Column, Integer, String, Float, Numeric, Text
from sqlalchemy.orm import relationship
from utils.db import Base

class Machine(Base):
    __tablename__ = "machines"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    description = Column(Text)
    price = Column(Float, nullable=False)
    condition = Column(String, nullable=False)
    hours_used = Column(Numeric(10,2), nullable=True)
    seo_title = Column(String, nullable=True)
    seo_description = Column(String, nullable=True)
    best_for = Column(Text, nullable=True)
    not_for = Column(Text, nullable=True)
    key_benefits = Column(Text, nullable=True)
    common_uses = Column(Text, nullable=True)
    faq = Column(Text, nullable=True)
    comparison_notes = Column(Text, nullable=True)
    slug = Column(String, unique=True, index=True, nullable=True)

    images = relationship("Image", back_populates="machine")