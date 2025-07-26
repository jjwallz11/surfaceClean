# app/api/faqs_routes.py

from fastapi import APIRouter, Depends, HTTPException, Path
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.dependencies.db import get_db
from app.dependencies.auth import get_current_user
from app.models.faqs import FAQ
from app.schemas.faqs import FAQCreate, FAQUpdate

router = APIRouter()

# READ
@router.get("/")
async def get_faqs(session: AsyncSession = Depends(get_db)):
    result = await session.execute(select(FAQ))
    return result.scalars().all()

# CREATE
@router.post("/")
async def create_faq(data: FAQCreate, session: AsyncSession = Depends(get_db), user=Depends(get_current_user)):
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
    session: AsyncSession = Depends(get_db),
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
    session: AsyncSession = Depends(get_db),
    user=Depends(get_current_user)
):
    faq = await session.get(FAQ, faq_id)
    if not faq:
        raise HTTPException(status_code=404, detail="FAQ not found")

    await session.delete(faq)
    await session.commit()
    return {"message": "FAQ deleted"}