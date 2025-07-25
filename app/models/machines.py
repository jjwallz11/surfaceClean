# app/models/machines.py

from sqlalchemy import Column, Integer, String, Float, Numeric, Text
from sqlalchemy.orm import relationship
from models.db import Base

class Machine(Base):
    __tablename__ = "machines"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    description = Column(Text)
    price = Column(Float, nullable=False)
    hours_used = Column(Numeric(10,2), nullable=True)

    images = relationship("Image", back_populates="machine")