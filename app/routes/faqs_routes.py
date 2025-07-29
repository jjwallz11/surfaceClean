# app/api/faqs_routes.py

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from utils.db import get_async_db
from utils.auth import get_current_user
from models.faqs import FAQ
from schemas.faqs import FAQCreate, FAQUpdate
from typing import List

router = APIRouter()

# READ
@router.get("/", response_model=List[FAQCreate])
async def get_faqs(db: AsyncSession = Depends(get_async_db)):
    result = await db.execute(select(FAQ))
    return result.scalars().all()

# CREATE
@router.post("/", response_model=FAQCreate)
async def create_faq(
    data: FAQCreate,
    db: AsyncSession = Depends(get_async_db),
    user=Depends(get_current_user),
):
    faq = FAQ(**data.dict())
    db.add(faq)
    await db.commit()
    await db.refresh(faq)
    return faq

# UPDATE
@router.patch("/{faq_id}", response_model=FAQCreate)
async def update_faq(
    faq_id: int,
    data: FAQUpdate,
    db: AsyncSession = Depends(get_async_db),
    user=Depends(get_current_user),
):
    result = await db.execute(select(FAQ).where(FAQ.id == faq_id))
    faq = result.scalar_one_or_none()

    if not faq:
        raise HTTPException(status_code=404, detail="FAQ not found")

    for key, value in data.dict(exclude_unset=True).items():
        setattr(faq, key, value)

    await db.commit()
    await db.refresh(faq)
    return faq

# DELETE
@router.delete("/{faq_id}")
async def delete_faq(
    faq_id: int,
    db: AsyncSession = Depends(get_async_db),
    user=Depends(get_current_user),
):
    result = await db.execute(select(FAQ).where(FAQ.id == faq_id))
    faq = result.scalar_one_or_none()

    if not faq:
        raise HTTPException(status_code=404, detail="FAQ not found")

    await db.delete(faq)
    await db.commit()
    return {"message": "FAQ deleted"}