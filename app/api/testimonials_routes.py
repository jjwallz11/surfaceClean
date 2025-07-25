# app/api/testimonials_routes.py

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from dependencies.db import get_session
from dependencies.auth import get_current_user
from models.testimonials import Testimonial
from schemas.testimonials import TestimonialCreate, TestimonialUpdate

router = APIRouter()

# READ
@router.get("/")
async def get_testimonials(session: AsyncSession = Depends(get_session)):
    result = await session.execute(select(Testimonial))
    return result.scalars().all()

# CREATE
@router.post("/")
async def create_testimonial(
    data: TestimonialCreate,
    session: AsyncSession = Depends(get_session),
    user=Depends(get_current_user)
):
    testimonial = Testimonial(**data.dict())
    session.add(testimonial)
    await session.commit()
    await session.refresh(testimonial)
    return testimonial

# UPDATE
@router.patch("/{testimonial_id}")
async def update_testimonial(
    testimonial_id: int,
    data: TestimonialUpdate,
    session: AsyncSession = Depends(get_session),
    user=Depends(get_current_user)
):
    testimonial = await session.get(Testimonial, testimonial_id)
    if not testimonial:
        raise HTTPException(status_code=404, detail="Testimonial not found")

    for key, value in data.dict(exclude_unset=True).items():
        setattr(testimonial, key, value)

    await session.commit()
    await session.refresh(testimonial)
    return testimonial

# DELETE
@router.delete("/{testimonial_id}")
async def delete_testimonial(
    testimonial_id: int,
    session: AsyncSession = Depends(get_session),
    user=Depends(get_current_user)
):
    testimonial = await session.get(Testimonial, testimonial_id)
    if not testimonial:
        raise HTTPException(status_code=404, detail="Testimonial not found")

    await session.delete(testimonial)
    await session.commit()
    return {"message": "Testimonial deleted"}