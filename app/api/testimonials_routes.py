from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.dependencies.db import get_session
from app.models.testimonials import Testimonial
from app.schemas.testimonials import TestimonialCreate

router = APIRouter()

@router.get("/")
async def get_testimonials(session: AsyncSession = Depends(get_session)):
    result = await session.execute(Testimonial.__table__.select())
    return result.scalars().all()

@router.post("/")
async def create_testimonial(data: TestimonialCreate, session: AsyncSession = Depends(get_session)):
    testimonial = Testimonial(**data.dict())
    session.add(testimonial)
    await session.commit()
    await session.refresh(testimonial)
    return testimonial