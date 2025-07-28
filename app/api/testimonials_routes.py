# app/api/testimonials_routes.py

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import select
from app.dependencies.db import get_db
from app.dependencies.auth import get_current_user
from app.models.testimonials import Testimonial
from app.schemas.testimonials import TestimonialCreate, TestimonialUpdate

router = APIRouter()

# READ
@router.get("/")
def get_testimonials(session: Session = Depends(get_db)):
    result = session.execute(select(Testimonial))
    return result.scalars().all()

# CREATE
@router.post("/")
def create_testimonial(
    data: TestimonialCreate,
    session: Session = Depends(get_db),
    user=Depends(get_current_user)
):
    testimonial = Testimonial(**data.dict())
    session.add(testimonial)
    session.commit()
    session.refresh(testimonial)
    return testimonial

# UPDATE
@router.patch("/{testimonial_id}")
def update_testimonial(
    testimonial_id: int,
    data: TestimonialUpdate,
    session: Session = Depends(get_db),
    user=Depends(get_current_user)
):
    testimonial = session.get(Testimonial, testimonial_id)
    if not testimonial:
        raise HTTPException(status_code=404, detail="Testimonial not found")

    for key, value in data.dict(exclude_unset=True).items():
        setattr(testimonial, key, value)

    session.commit()
    session.refresh(testimonial)
    return testimonial

# DELETE
@router.delete("/{testimonial_id}")
def delete_testimonial(
    testimonial_id: int,
    session: Session = Depends(get_db),
    user=Depends(get_current_user)
):
    testimonial = session.get(Testimonial, testimonial_id)
    if not testimonial:
        raise HTTPException(status_code=404, detail="Testimonial not found")

    session.delete(testimonial)
    session.commit()
    return {"message": "Testimonial deleted"}