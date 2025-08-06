# app/api/testimonials_routes.py

from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from utils.db import get_async_db
from .auth_routes import get_current_user
from utils.csrf import verify_csrf
from models.testimonials import Testimonial
from schemas.testimonials import TestimonialCreate, TestimonialUpdate, TestimonialResponse
from typing import List

router = APIRouter()

@router.get("/", response_model=List[TestimonialResponse])
async def get_testimonials(db: AsyncSession = Depends(get_async_db)):
    result = await db.execute(select(Testimonial))
    return result.scalars().all()

@router.post("/", response_model=TestimonialCreate)
async def create_testimonial(
    request: Request,
    data: TestimonialCreate,
    db: AsyncSession = Depends(get_async_db),
    user=Depends(get_current_user)
):
    verify_csrf(request)
    testimonial = Testimonial(**data.dict())
    db.add(testimonial)
    await db.commit()
    await db.refresh(testimonial)
    return testimonial

@router.patch("/{testimonial_id}", response_model=TestimonialUpdate)
async def update_testimonial(
    request: Request,
    testimonial_id: int,
    data: TestimonialUpdate,
    db: AsyncSession = Depends(get_async_db),
    user=Depends(get_current_user)
):
    verify_csrf(request)
    result = await db.execute(select(Testimonial).where(Testimonial.id == testimonial_id))
    testimonial = result.scalar_one_or_none()

    if not testimonial:
        raise HTTPException(status_code=404, detail="Testimonial not found")

    for key, value in data.dict(exclude_unset=True).items():
        setattr(testimonial, key, value)

    await db.commit()
    await db.refresh(testimonial)
    return testimonial

@router.delete("/{testimonial_id}")
async def delete_testimonial(
    request: Request,
    testimonial_id: int,
    db: AsyncSession = Depends(get_async_db),
    user=Depends(get_current_user)
):
    verify_csrf(request)
    result = await db.execute(select(Testimonial).where(Testimonial.id == testimonial_id))
    testimonial = result.scalar_one_or_none()

    if not testimonial:
        raise HTTPException(status_code=404, detail="Testimonial not found")

    await db.delete(testimonial)
    await db.commit()
    return {"message": "Testimonial deleted"}