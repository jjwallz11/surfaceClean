# app/seeds/images.py

from models import Image
from sqlalchemy.orm import Session

def seed_images(db: Session):
    images = [
        Image(
            url="https://example.com/machine1_img1.jpg",
            machine_id=1,
            description="Front view of refurbished Tennant T5"
        ),
        Image(
            url="https://example.com/machine1_img2.jpg",
            machine_id=1
            # no description (test how null is handled)
        ),
        Image(
            url="https://example.com/part1_img1.jpg",
            part_id=1,
            description="Replacement squeegee blade – fits T3 and T5"
        )
    ]

    db.add_all(images)

def undo_images(db: Session):
    db.query(Image).delete()