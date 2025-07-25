# app/api/faqs_routes.py

from fastapi import APIRouter, Depends, HTTPException, Path
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from dependencies.db import get_session
from dependencies.auth import get_current_user
from models.faqs import FAQ
from schemas.faqs import FAQCreate, FAQUpdate

router = APIRouter()

# READ
@router.get("/")
async def get_faqs(session: AsyncSession = Depends(get_session)):
    result = await session.execute(select(FAQ))
    return result.scalars().all()

# CREATE
@router.post("/")
async def create_faq(data: FAQCreate, session: AsyncSession = Depends(get_session), user=Depends(get_current_user)):
    faq = FAQ(**data.dict())
    session.add(faq)
    await session.commit()
    await session.refresh(faq)
    return faq

# UPDATE
@router.patch("/{faq_id}")
async def update_faq(
    faq_id: int,
    data: FAQUpdate,
    session: AsyncSession = Depends(get_session),
    user=Depends(get_current_user)
):
    faq = await session.get(FAQ, faq_id)
    if not faq:
        raise HTTPException(status_code=404, detail="FAQ not found")

    for key, value in data.dict(exclude_unset=True).items():
        setattr(faq, key, value)

    await session.commit()
    await session.refresh(faq)
    return faq

# DELETE
@router.delete("/{faq_id}")
async def delete_faq(
    faq_id: int,
    session: AsyncSession = Depends(get_session),
    user=Depends(get_current_user)
):
    faq = await session.get(FAQ, faq_id)
    if not faq:
        raise HTTPException(status_code=404, detail="FAQ not found")

    await session.delete(faq)
    await session.commit()
    return {"message": "FAQ deleted"}