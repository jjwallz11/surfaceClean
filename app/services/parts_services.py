# app/services/parts_services.py

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from models.parts import Part
from schemas.parts import PartCreate, PartUpdate
from typing import Optional, List

async def get_all_parts(db: AsyncSession) -> List[Part]:
    result = await db.execute(select(Part))
    return result.scalars().all()

async def create_part(db: AsyncSession, data: PartCreate) -> Part:
    new_part = Part(**data.dict())
    db.add(new_part)
    await db.commit()
    await db.refresh(new_part)
    return new_part

async def update_part(db: AsyncSession, part_id: int, data: PartUpdate) -> Optional[Part]:
    result = await db.execute(select(Part).where(Part.id == part_id))
    part = result.scalar_one_or_none()
    if not part:
        return None

    for key, value in data.dict(exclude_unset=True).items():
        setattr(part, key, value)

    await db.commit()
    await db.refresh(part)
    return part

async def delete_part(db: AsyncSession, part_id: int) -> Optional[Part]:
    result = await db.execute(select(Part).where(Part.id == part_id))
    part = result.scalar_one_or_none()
    if not part:
        return None

    await db.delete(part)
    await db.commit()
    return part