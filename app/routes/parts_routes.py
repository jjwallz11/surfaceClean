# app/api/parts_routes.py

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from utils.db import get_async_db
from utils.auth import get_current_user
from models.parts import Part
from schemas.parts import PartCreate, PartUpdate
from typing import List

router = APIRouter()

# READ
@router.get("/", response_model=List[PartCreate])
async def get_parts(
    db: AsyncSession = Depends(get_async_db)
):
    result = await db.execute(select(Part))
    return result.scalars().all()

# CREATE
@router.post("/", response_model=PartCreate)
async def create_part(
    data: PartCreate,
    db: AsyncSession = Depends(get_async_db),
    user=Depends(get_current_user)
):
    part = Part(**data.dict())
    db.add(part)
    await db.commit()
    await db.refresh(part)
    return part

# UPDATE
@router.patch("/{part_id}", response_model=PartCreate)
async def update_part(
    part_id: int,
    data: PartUpdate,
    db: AsyncSession = Depends(get_async_db),
    user=Depends(get_current_user)
):
    result = await db.execute(select(Part).where(Part.id == part_id))
    part = result.scalar_one_or_none()

    if not part:
        raise HTTPException(status_code=404, detail="Part not found")

    for key, value in data.dict(exclude_unset=True).items():
        setattr(part, key, value)

    await db.commit()
    await db.refresh(part)
    return part

# DELETE
@router.delete("/{part_id}")
async def delete_part(
    part_id: int,
    db: AsyncSession = Depends(get_async_db),
    user=Depends(get_current_user)
):
    result = await db.execute(select(Part).where(Part.id == part_id))
    part = result.scalar_one_or_none()

    if not part:
        raise HTTPException(status_code=404, detail="Part not found")

    await db.delete(part)
    await db.commit()
    return {"message": "Part deleted"}