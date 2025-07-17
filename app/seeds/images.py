# seeds/images.py

from app.models import Image
from sqlalchemy.ext.asyncio import AsyncSession

async def seed_images(session: AsyncSession):
    images = [
        Image(
            url="https://example.com/machine1_img1.jpg",
            machine_id=1
        ),
        Image(
            url="https://example.com/machine1_img2.jpg",
            machine_id=1
        ),
        Image(
            url="https://example.com/part1_img1.jpg",
            part_id=1
        )
    ]

    session.add_all(images)
    await session.commit()