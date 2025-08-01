# app/api/images_routes.py

from fastapi import APIRouter, Depends, HTTPException, File, UploadFile, Form
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from utils.db import get_async_db
from utils.auth import get_current_user
from utils.cloudinary import upload_image
from models.images import Image
from schemas.images import ImageCreate, ImageUpdate, ImageResponse
from typing import List

router = APIRouter()

# READ all
@router.get("/", response_model=List[ImageCreate])
async def get_images(
    db: AsyncSession = Depends(get_async_db)
):
    result = await db.execute(select(Image))
    return result.scalars().all()

# CREATE
@router.post("/", response_model=ImageResponse)
async def create_image(
    file: UploadFile = File(...),
    description: str = Form(...),
    machine_id: int = Form(...),
    db: AsyncSession = Depends(get_async_db),
    user=Depends(get_current_user)
):
    # Upload to Cloudinary
    cloudinary_url = await upload_image(file.file, user.email)

    # Save to DB
    new_image = Image(
        url=cloudinary_url,
        description=description,
        machine_id=machine_id
    )
    db.add(new_image)
    await db.commit()
    await db.refresh(new_image)
    return new_image

# UPDATE
@router.patch("/{image_id}", response_model=ImageResponse)
async def update_image(
    image_id: int,
    data: ImageUpdate,
    db: AsyncSession = Depends(get_async_db),
    user=Depends(get_current_user)
):
    result = await db.execute(select(Image).where(Image.id == image_id))
    image = result.scalar_one_or_none()

    if not image:
        raise HTTPException(status_code=404, detail="Image not found")

    for key, value in data.dict(exclude_unset=True).items():
        setattr(image, key, value)

    await db.commit()
    await db.refresh(image)
    return image

# DELETE
@router.delete("/{image_id}")
async def delete_image(
    image_id: int,
    db: AsyncSession = Depends(get_async_db),
    user=Depends(get_current_user)
):
    result = await db.execute(select(Image).where(Image.id == image_id))
    image = result.scalar_one_or_none()

    if not image:
        raise HTTPException(status_code=404, detail="Image not found")

    await db.delete(image)
    await db.commit()
    return {"message": "Image deleted"}