# app/schemas/machines.py

from pydantic import BaseModel
from typing import Optional, List
from decimal import Decimal
from .images import ImageResponse


class MachineBase(BaseModel):
    # fields that can be patched
    name: Optional[str] = None
    price: Optional[float] = None
    condition: Optional[str] = None
    description: Optional[str] = None
    hours_used: Optional[Decimal] = None
    seo_title: Optional[str] = None
    seo_description: Optional[str] = None
    best_for: Optional[str] = None
    not_for: Optional[str] = None
    key_benefits: Optional[str] = None
    common_uses: Optional[str] = None
    faq: Optional[str] = None
    comparison_notes: Optional[str] = None
    slug: Optional[str] = None


class MachineCreate(BaseModel):
    # required when creating
    name: str
    price: float
    condition: str
    description: Optional[str] = None
    hours_used: Optional[Decimal] = None
    seo_title: Optional[str] = None
    seo_description: Optional[str] = None
    best_for: Optional[str] = None
    not_for: Optional[str] = None
    key_benefits: Optional[str] = None
    common_uses: Optional[str] = None
    faq: Optional[str] = None
    comparison_notes: Optional[str] = None
    slug: Optional[str] = None


class MachineUpdate(MachineBase):
    # all optional – inherits from MachineBase
    pass


class MachineResponse(BaseModel):
    id: int
    name: str
    price: float
    condition: str
    description: Optional[str] = None
    hours_used: Optional[Decimal] = None
    images: List[ImageResponse] = []
    seo_title: Optional[str] = None
    seo_description: Optional[str] = None
    best_for: Optional[str] = None
    not_for: Optional[str] = None
    key_benefits: Optional[str] = None
    common_uses: Optional[str] = None
    faq: Optional[str] = None
    comparison_notes: Optional[str] = None
    slug: Optional[str] = None

    class Config:
        model_config = {"from_attributes": True}
