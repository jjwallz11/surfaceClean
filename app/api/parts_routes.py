# app/api/parts_routes.py

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import select
from app.dependencies.db import get_db
from app.dependencies.auth import get_current_user
from app.models.parts import Part
from app.schemas.parts import PartCreate, PartUpdate

router = APIRouter()

# READ
@router.get("/")
def get_parts(session: Session = Depends(get_db)):
    result = session.execute(select(Part))
    return result.scalars().all()

# CREATE
@router.post("/")
def create_part(
    data: PartCreate,
    session: Session = Depends(get_db),
    user=Depends(get_current_user)
):
    part = Part(**data.dict())
    session.add(part)
    session.commit()
    session.refresh(part)
    return part

# UPDATE
@router.patch("/{part_id}")
def update_part(
    part_id: int,
    data: PartUpdate,
    session: Session = Depends(get_db),
    user=Depends(get_current_user)
):
    part = session.get(Part, part_id)
    if not part:
        raise HTTPException(status_code=404, detail="Part not found")

    for key, value in data.dict(exclude_unset=True).items():
        setattr(part, key, value)

    session.commit()
    session.refresh(part)
    return part

# DELETE
@router.delete("/{part_id}")
def delete_part(
    part_id: int,
    session: Session = Depends(get_db),
    user=Depends(get_current_user)
):
    part = session.get(Part, part_id)
    if not part:
        raise HTTPException(status_code=404, detail="Part not found")

    session.delete(part)
    session.commit()
    return {"message": "Part deleted"}