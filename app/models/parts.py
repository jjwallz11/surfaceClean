from sqlalchemy import Column, Integer, String, Float, Text, ForeignKey
from sqlalchemy.orm import relationship
from app.db import Base

class Part(Base):
    __tablename__ = "parts"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    description = Column(Text)
    price = Column(Float, nullable=False)
    quantity = Column(Integer, nullable=False, default=1)
    owner_id = Column(Integer, ForeignKey("users.id"))

    owner = relationship("User", back_populates="parts")
    images = relationship("Image", back_populates="part")