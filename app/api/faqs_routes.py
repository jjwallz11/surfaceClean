# app/api/faqs_routes.py

from fastapi import APIRouter, Depends, HTTPException, Path
from sqlalchemy.orm import Session
from sqlalchemy import select
from app.dependencies.db import get_db
from app.dependencies.auth import get_current_user
from app.models.faqs import FAQ
from app.schemas.faqs import FAQCreate, FAQUpdate

router = APIRouter()

# READ
@router.get("/")
def get_faqs(session: Session = Depends(get_db)):
    result = session.execute(select(FAQ))
    return result.scalars().all()

# CREATE
@router.post("/")
def create_faq(data: FAQCreate, session: Session = Depends(get_db), user=Depends(get_current_user)):
    faq = FAQ(**data.dict())
    session.add(faq)
    session.commit()
    session.refresh(faq)
    return faq

# UPDATE
@router.patch("/{faq_id}")
def update_faq(
    faq_id: int,
    data: FAQUpdate,
    session: Session = Depends(get_db),
    user=Depends(get_current_user)
):
    faq = session.get(FAQ, faq_id)
    if not faq:
        raise HTTPException(status_code=404, detail="FAQ not found")

    for key, value in data.dict(exclude_unset=True).items():
        setattr(faq, key, value)

    session.commit()
    session.refresh(faq)
    return faq

# DELETE
@router.delete("/{faq_id}")
def delete_faq(
    faq_id: int,
    session: Session = Depends(get_db),
    user=Depends(get_current_user)
):
    faq = session.get(FAQ, faq_id)
    if not faq:
        raise HTTPException(status_code=404, detail="FAQ not found")

    session.delete(faq)
    session.commit()
    return {"message": "FAQ deleted"}