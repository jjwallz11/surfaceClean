# app/services/images_services.py

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from models.images import Image
from schemas.images import ImageCreate, ImageUpdate
from typing import Optional, List

async def create_image(db: AsyncSession, image_data: ImageCreate) -> Image:
    image = Image(**image_data.dict())
    db.add(image)
    await db.commit()
    await db.refresh(image)
    return image

async def get_all_images(db: AsyncSession) -> List[Image]:
    result = await db.execute(select(Image))
    return result.scalars().all()

async def update_image(db: AsyncSession, image_id: int, image_data: ImageUpdate) -> Optional[Image]:
    result = await db.execute(select(Image).where(Image.id == image_id))
    image = result.scalar_one_or_none()
    if not image:
        return None

    for key, value in image_data.dict(exclude_unset=True).items():
        setattr(image, key, value)

    await db.commit()
    await db.refresh(image)
    return image

async def delete_image(db: AsyncSession, image_id: int) -> Optional[Image]:
    result = await db.execute(select(Image).where(Image.id == image_id))
    image = result.scalar_one_or_none()
    if not image:
        return None

    await db.delete(image)
    await db.commit()
    return image