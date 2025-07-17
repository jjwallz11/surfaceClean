from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.dependencies.db import get_session
from app.models.faqs import FAQ
from app.schemas.faqs import FAQCreate

router = APIRouter()

@router.get("/")
async def get_faqs(session: AsyncSession = Depends(get_session)):
    result = await session.execute(FAQ.__table__.select())
    return result.scalars().all()

@router.post("/")
async def create_faq(data: FAQCreate, session: AsyncSession = Depends(get_session)):
    faq = FAQ(**data.dict())
    session.add(faq)
    await session.commit()
    await session.refresh(faq)
    return faq