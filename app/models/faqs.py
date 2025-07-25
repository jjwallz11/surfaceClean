# app/models/faqs.py

from sqlalchemy import Column, Integer, String, Text
from models.db import Base

class FAQ(Base):
    __tablename__ = "faqs"

    id = Column(Integer, primary_key=True, index=True)
    question = Column(Text, nullable=False)
    answer = Column(Text, nullable=False)