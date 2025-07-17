from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.dependencies.db import get_session
from app.dependencies.auth import get_current_user
from app.models.images import Image
from app.schemas.images import ImageCreate

router = APIRouter()

@router.get("/")
async def get_images(session: AsyncSession = Depends(get_session)):
    result = await session.execute(Image.__table__.select())
    return result.scalars().all()

@router.post("/")
async def create_image(data: ImageCreate, session: AsyncSession = Depends(get_session), user=Depends(get_current_user)):
    image = Image(**data.dict())
    session.add(image)
    await session.commit()
    await session.refresh(image)
    return image