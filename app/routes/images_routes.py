# app/api/images_routes.py

from fastapi import APIRouter, Depends, HTTPException, File, UploadFile, Form, Request
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from utils.db import get_async_db
from .auth_routes import get_current_user
from utils.cloudinary import upload_image, delete_image as delete_from_cloudinary
from utils.csrf import verify_csrf
from models.images import Image
from schemas.images import ImageCreate, ImageUpdate, ImageResponse
from typing import List

router = APIRouter()

@router.get("/", response_model=List[ImageResponse])
async def get_images(db: AsyncSession = Depends(get_async_db)):
    result = await db.execute(select(Image))
    return result.scalars().all()

@router.post("/", response_model=ImageResponse)
async def create_image(
    request: Request,
    file: UploadFile = File(...),
    description: str = Form(...),
    machine_id: int = Form(...),
    db: AsyncSession = Depends(get_async_db),
    user=Depends(get_current_user)
):
    verify_csrf(request)
    cloudinary_result = await upload_image(file.file, user.email)
    new_image = Image(
        url=cloudinary_result["secure_url"],
        public_id=cloudinary_result["public_id"],
        description=description,
        machine_id=machine_id
    )
    db.add(new_image)
    await db.commit()
    await db.refresh(new_image)
    return new_image

@router.patch("/{image_id}", response_model=ImageResponse)
async def update_image(
    request: Request,
    image_id: int,
    data: ImageUpdate,
    db: AsyncSession = Depends(get_async_db),
    user=Depends(get_current_user)
):
    verify_csrf(request)
    result = await db.execute(select(Image).where(Image.id == image_id))
    image = result.scalar_one_or_none()

    if not image:
        raise HTTPException(status_code=404, detail="Image not found")

    for key, value in data.dict(exclude_unset=True).items():
        setattr(image, key, value)

    await db.commit()
    await db.refresh(image)
    return image

@router.delete("/{image_id}")
async def delete_image(
    request: Request,
    image_id: int,
    db: AsyncSession = Depends(get_async_db),
    user=Depends(get_current_user)
):
    verify_csrf(request)
    result = await db.execute(select(Image).where(Image.id == image_id))
    image = result.scalar_one_or_none()

    if not image:
        raise HTTPException(status_code=404, detail="Image not found")

    if image.url:
        await delete_from_cloudinary(image.url)

    await db.delete(image)
    await db.commit()

    return {"message": "Image deleted"}