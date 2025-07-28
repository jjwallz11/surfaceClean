# app/api/images_routes.py

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import select
from app.dependencies.db import get_db
from app.dependencies.auth import get_current_user
from app.models.images import Image
from app.schemas.images import ImageCreate, ImageUpdate

router = APIRouter()

# READ all
@router.get("/")
def get_images(session: Session = Depends(get_db)):
    result = session.execute(select(Image))
    return result.scalars().all()

# CREATE
@router.post("/")
def create_image(
    data: ImageCreate,
    session: Session = Depends(get_db),
    user=Depends(get_current_user)
):
    image = Image(**data.dict())
    session.add(image)
    session.commit()
    session.refresh(image)
    return image

# UPDATE
@router.patch("/{image_id}")
def update_image(
    image_id: int,
    data: ImageUpdate,
    session: Session = Depends(get_db),
    user=Depends(get_current_user)
):
    image = session.get(Image, image_id)
    if not image:
        raise HTTPException(status_code=404, detail="Image not found")

    for key, value in data.dict(exclude_unset=True).items():
        setattr(image, key, value)

    session.commit()
    session.refresh(image)
    return image

# DELETE
@router.delete("/{image_id}")
def delete_image(
    image_id: int,
    session: Session = Depends(get_db),
    user=Depends(get_current_user)
):
    image = session.get(Image, image_id)
    if not image:
        raise HTTPException(status_code=404, detail="Image not found")

    session.delete(image)
    session.commit()
    return {"message": "Image deleted"}