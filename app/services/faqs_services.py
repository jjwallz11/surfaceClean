# app/services/faqs_services.py

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from typing import Optional, List
from models.faqs import FAQ
from schemas.faqs import FAQCreate, FAQUpdate

async def get_all_faqs(db: AsyncSession) -> List[FAQ]:
    result = await db.execute(select(FAQ))
    return result.scalars().all()

async def create_faq(db: AsyncSession, faq_data: FAQCreate) -> FAQ:
    faq = FAQ(**faq_data.dict())
    db.add(faq)
    await db.commit()
    await db.refresh(faq)
    return faq

async def update_faq(db: AsyncSession, faq_id: int, faq_data: FAQUpdate) -> Optional[FAQ]:
    result = await db.execute(select(FAQ).where(FAQ.id == faq_id))
    faq = result.scalar_one_or_none()
    if not faq:
        return None

    for key, value in faq_data.dict(exclude_unset=True).items():
        setattr(faq, key, value)

    await db.commit()
    await db.refresh(faq)
    return faq

async def delete_faq(db: AsyncSession, faq_id: int) -> bool:
    result = await db.execute(select(FAQ).where(FAQ.id == faq_id))
    faq = result.scalar_one_or_none()
    if not faq:
        return False

    await db.delete(faq)
    await db.commit()
    return True