# app/models/images.py

from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from utils.db import Base


class Image(Base):
    __tablename__ = "images"

    id = Column(Integer, primary_key=True, index=True)
    url = Column(String, nullable=False)
    description = Column(String, nullable=True)
    machine_id = Column(Integer, ForeignKey("machines.id"), nullable=True)
    public_id = Column(String, nullable=False)

    machine = relationship("Machine", back_populates="images")