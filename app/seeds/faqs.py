# seeds/faqs.py

from app.models import FAQ
from sqlalchemy.ext.asyncio import AsyncSession

async def seed_faqs(session: AsyncSession):
    faqs = [
        FAQ(
            question="How long does shipping take?",
            answer="Shipping typically takes 5-7 business days."
        ),
        FAQ(
            question="Are the machines refurbished?",
            answer="Yes, all machines are cleaned, tested, and refurbished before resale."
        ),
        FAQ(
            question="Do you offer warranties?",
            answer="A limited 30-day warranty is provided on all machines unless otherwise specified."
        )
    ]

    session.add_all(faqs)
    await session.commit()