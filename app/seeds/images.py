from app.models import Image
from sqlalchemy.orm import Session

def seed_images(db: Session):
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

    db.add_all(images)

def undo_images(db: Session):
    db.query(Image).delete()