# app/api/images_routes.py

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from dependencies.db import get_session
from dependencies.auth import get_current_user
from models.images import Image
from schemas.images import ImageCreate, ImageUpdate

router = APIRouter()

# READ all
@router.get("/")
async def get_images(session: AsyncSession = Depends(get_session)):
    result = await session.execute(select(Image))
    return result.scalars().all()

# CREATE
@router.post("/")
async def create_image(
    data: ImageCreate,
    session: AsyncSession = Depends(get_session),
    user=Depends(get_current_user)
):
    image = Image(**data.dict())
    session.add(image)
    await session.commit()
    await session.refresh(image)
    return image

# UPDATE
@router.patch("/{image_id}")
async def update_image(
    image_id: int,
    data: ImageUpdate,
    session: AsyncSession = Depends(get_session),
    user=Depends(get_current_user)
):
    image = await session.get(Image, image_id)
    if not image:
        raise HTTPException(status_code=404, detail="Image not found")

    for key, value in data.dict(exclude_unset=True).items():
        setattr(image, key, value)

    await session.commit()
    await session.refresh(image)
    return image

# DELETE
@router.delete("/{image_id}")
async def delete_image(
    image_id: int,
    session: AsyncSession = Depends(get_session),
    user=Depends(get_current_user)
):
    image = await session.get(Image, image_id)
    if not image:
        raise HTTPException(status_code=404, detail="Image not found")

    await session.delete(image)
    await session.commit()
    return {"message": "Image deleted"}