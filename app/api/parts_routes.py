# app/api/parts_routes.py

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from dependencies.db import get_session
from dependencies.auth import get_current_user
from models.parts import Part
from schemas.parts import PartCreate, PartUpdate

router = APIRouter()

# READ
@router.get("/")
async def get_parts(session: AsyncSession = Depends(get_session)):
    result = await session.execute(select(Part))
    return result.scalars().all()

# CREATE
@router.post("/")
async def create_part(
    data: PartCreate,
    session: AsyncSession = Depends(get_session),
    user=Depends(get_current_user)
):
    part = Part(**data.dict())
    session.add(part)
    await session.commit()
    await session.refresh(part)
    return part

# UPDATE
@router.patch("/{part_id}")
async def update_part(
    part_id: int,
    data: PartUpdate,
    session: AsyncSession = Depends(get_session),
    user=Depends(get_current_user)
):
    part = await session.get(Part, part_id)
    if not part:
        raise HTTPException(status_code=404, detail="Part not found")

    for key, value in data.dict(exclude_unset=True).items():
        setattr(part, key, value)

    await session.commit()
    await session.refresh(part)
    return part

# DELETE
@router.delete("/{part_id}")
async def delete_part(
    part_id: int,
    session: AsyncSession = Depends(get_session),
    user=Depends(get_current_user)
):
    part = await session.get(Part, part_id)
    if not part:
        raise HTTPException(status_code=404, detail="Part not found")

    await session.delete(part)
    await session.commit()
    return {"message": "Part deleted"}