# seeds/faqs.py

from app.models import FAQ
from sqlalchemy.orm import Session

def seed_faqs(db: Session):
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

    db.add_all(faqs)

def undo_faqs(db: Session):
    db.query(FAQ).delete()