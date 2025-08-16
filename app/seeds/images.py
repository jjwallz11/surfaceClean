# app/seeds/images.py

import asyncio
from sqlalchemy import text
from utils.db import AsyncSessionLocal, Base, engine
from models.images import Image

async def seed_images():
    # Ensure schema exists
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    async with AsyncSessionLocal() as db:
        images = []

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