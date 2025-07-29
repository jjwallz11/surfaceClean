# app/services/testimonials_services.py

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from models.testimonials import Testimonial
from schemas.testimonials import TestimonialCreate, TestimonialUpdate
from typing import Optional, List

async def get_all_testimonials(db: AsyncSession) -> List[Testimonial]:
    result = await db.execute(select(Testimonial))
    return result.scalars().all()

async def create_testimonial(db: AsyncSession, data: TestimonialCreate) -> Testimonial:
    new_testimonial = Testimonial(**data.dict())
    db.add(new_testimonial)
    await db.commit()
    await db.refresh(new_testimonial)
    return new_testimonial

async def update_testimonial(db: AsyncSession, testimonial_id: int, data: TestimonialUpdate) -> Optional[Testimonial]:
    result = await db.execute(select(Testimonial).where(Testimonial.id == testimonial_id))
    testimonial = result.scalar_one_or_none()
    if not testimonial:
        return None

    for key, value in data.dict(exclude_unset=True).items():
        setattr(testimonial, key, value)

    await db.commit()
    await db.refresh(testimonial)
    return testimonial

async def delete_testimonial(db: AsyncSession, testimonial_id: int) -> Optional[Testimonial]:
    result = await db.execute(select(Testimonial).where(Testimonial.id == testimonial_id))
    testimonial = result.scalar_one_or_none()
    if not testimonial:
        return None

    await db.delete(testimonial)
    await db.commit()
    return testimonial