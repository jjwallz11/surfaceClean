# app/seeds/testimonials.py

from app.models import Testimonial
from sqlalchemy.orm import Session

def seed_testimonials(db: Session):
    testimonials = [
        Testimonial(
            author_name="Mike",
            stars=5,
            notables="Punctuality, Communication, Pricing, Item Description",
            content="Super nice honest person"
        ),
        Testimonial(
            author_name="Evangeline",
            stars=5,
            notables="Punctuality, Communication, Pricing, Item Description",
            content=None
        ),
        Testimonial(
            author_name="Dillion",
            stars=5,
            notables="Punctuality, Communication, Pricing, Item Description",
            content=None
        ),
        Testimonial(
            author_name="James",
            stars=5,
            notables="Punctuality, Friendliness, Communication, Reliability, Pricing, Item Description",
            content=None
        ),
        Testimonial(
            author_name="Juan",
            stars=5,
            notables=None,
            content=None
        ),
    ]

    db.add_all(testimonials)

def undo_testimonials(db: Session):
    db.query(Testimonial).delete()