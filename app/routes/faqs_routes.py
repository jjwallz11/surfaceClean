# app/api/faqs_routes.py

from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from utils.db import get_async_db
from .auth_routes import get_current_user
from utils.csrf import verify_csrf
from models.faqs import FAQ
from schemas.faqs import FAQCreate, FAQUpdate, FAQResponse
from datetime import datetime
from sqlalchemy import or_
from typing import List

router = APIRouter()

@router.get("/live", response_model=List[FAQResponse])
async def get_live_faqs(db: AsyncSession = Depends(get_async_db)):
    today = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
    result = await db.execute(
        select(FAQ).where(
            or_(
                FAQ.scheduled_post_date == None,
                FAQ.scheduled_post_date <= today
            )
        )
    )
    return result.scalars().all()

@router.get("/", response_model=List[FAQCreate])
async def get_faqs(db: AsyncSession = Depends(get_async_db)):
    result = await db.execute(select(FAQ))
    return result.scalars().all()

@router.post("/", response_model=FAQCreate)
async def create_faq(
    request: Request,
    data: FAQCreate,
    db: AsyncSession = Depends(get_async_db),
    user=Depends(get_current_user),
):
    verify_csrf(request)
    faq = FAQ(**data.dict())
    db.add(faq)
    await db.commit()
    await db.refresh(faq)
    return faq

@router.patch("/{faq_id}", response_model=FAQCreate)
async def update_faq(
    request: Request,
    faq_id: int,
    data: FAQUpdate,
    db: AsyncSession = Depends(get_async_db),
    user=Depends(get_current_user),
):
    verify_csrf(request)
    result = await db.execute(select(FAQ).where(FAQ.id == faq_id))
    faq = result.scalar_one_or_none()

    if not faq:
        raise HTTPException(status_code=404, detail="FAQ not found")

    for key, value in data.dict(exclude_unset=True).items():
        setattr(faq, key, value)

    await db.commit()
    await db.refresh(faq)
    return faq

@router.delete("/{faq_id}")
async def delete_faq(
    request: Request,
    faq_id: int,
    db: AsyncSession = Depends(get_async_db),
    user=Depends(get_current_user),
):
    verify_csrf(request)
    result = await db.execute(select(FAQ).where(FAQ.id == faq_id))
    faq = result.scalar_one_or_none()

    if not faq:
        raise HTTPException(status_code=404, detail="FAQ not found")

    await db.delete(faq)
    await db.commit()
    return {"message": "FAQ deleted"}