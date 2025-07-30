# app/api/testimonials_routes.py

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from utils.db import get_async_db
from utils.auth import get_current_user
from models.testimonials import Testimonial
from schemas.testimonials import TestimonialCreate, TestimonialUpdate, TestimonialResponse
from typing import List

router = APIRouter()

# READ
@router.get("/", response_model=List[TestimonialCreate])
async def get_testimonials(
    db: AsyncSession = Depends(get_async_db)
):
    result = await db.execute(select(Testimonial))
    return result.scalars().all()

# CREATE
@router.post("/", response_model=TestimonialCreate)
async def create_testimonial(
    data: TestimonialCreate,
    db: AsyncSession = Depends(get_async_db),
    user=Depends(get_current_user)
):
    testimonial = Testimonial(**data.dict())
    db.add(testimonial)
    await db.commit()
    await db.refresh(testimonial)
    return testimonial

# UPDATE
@router.patch("/{testimonial_id}", response_model=TestimonialResponse)
async def update_testimonial(
    testimonial_id: int,
    data: TestimonialUpdate,
    db: AsyncSession = Depends(get_async_db),
    user=Depends(get_current_user)
):
    result = await db.execute(select(Testimonial).where(Testimonial.id == testimonial_id))
    testimonial = result.scalar_one_or_none()

    if not testimonial:
        raise HTTPException(status_code=404, detail="Testimonial not found")

    for key, value in data.dict(exclude_unset=True).items():
        setattr(testimonial, key, value)

    await db.commit()
    await db.refresh(testimonial)
    return testimonial

# DELETE
@router.delete("/{testimonial_id}")
async def delete_testimonial(
    testimonial_id: int,
    db: AsyncSession = Depends(get_async_db),
    user=Depends(get_current_user)
):
    result = await db.execute(select(Testimonial).where(Testimonial.id == testimonial_id))
    testimonial = result.scalar_one_or_none()

    if not testimonial:
        raise HTTPException(status_code=404, detail="Testimonial not found")

    await db.delete(testimonial)
    await db.commit()
    return {"message": "Testimonial deleted"}