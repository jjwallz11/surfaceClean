# app/seeds/images.py

import asyncio
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession
from utils.db import AsyncSessionLocal, Base, engine
from models.images import Image

async def seed_images():
    # Ensure schema exists
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    async with AsyncSessionLocal() as db:
        images = [
            Image(
                url="https://example.com/machine1_img1.jpg",
                machine_id=1,
                description="Front view of refurbished Tennant T5"
            ),
            Image(
                url="https://example.com/machine1_img2.jpg",
                machine_id=1
                # No description – tests NULL handling
            ),
            Image(
                url="https://example.com/part1_img1.jpg",
                machine_id=1,
                description="Replacement squeegee blade – fits T3 and T5"
            )
        ]

        db.add_all(images)
        await db.commit()
        print("🖼️ Seeded images")

async def undo_images():
    async with AsyncSessionLocal() as db:
        await db.execute(text("DELETE FROM images"))
        await db.commit()
        print("🗑️ Deleted all images")

# Optional standalone runner
if __name__ == "__main__":
    asyncio.run(seed_images())