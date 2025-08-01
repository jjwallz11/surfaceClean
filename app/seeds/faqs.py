# app/seeds/faqs.py

import asyncio
from sqlalchemy import text
from utils.db import AsyncSessionLocal, Base, engine
from models.faqs import FAQ

async def seed_faqs():
    # Ensure schema exists
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    async with AsyncSessionLocal() as db:
        faqs = [
            FAQ(
                question="How long does shipping take?",
                answer="Shipping typically takes 5-7 business days.",
            ),
            FAQ(
                question="Are the machines refurbished?",
                answer="Yes, all machines are cleaned, tested, and refurbished before resale.",
                scheduled_post_date="08-5-2025"
            ),
            FAQ(
                question="Do you offer warranties?",
                answer="A limited 30-day warranty is provided on all machines unless otherwise specified.",
                scheduled_post_date="08-6-2025"
            )
        ]

        db.add_all(faqs)
        await db.commit()
        print("✅ Seeded FAQs")

async def undo_faqs():
    async with AsyncSessionLocal() as db:
        await db.execute(text("DELETE FROM faqs"))
        await db.commit()
        print("🗑️ Deleted all FAQs")

# Optional standalone runner
if __name__ == "__main__":
    asyncio.run(seed_faqs())