from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.dependencies.db import get_session
from app.dependencies.auth import get_current_user
from app.models.parts import Part
from app.schemas.parts import PartCreate

router = APIRouter()

@router.get("/")
async def get_parts(session: AsyncSession = Depends(get_session)):
    result = await session.execute(Part.__table__.select())
    return result.scalars().all()

@router.post("/")
async def create_part(data: PartCreate, session: AsyncSession = Depends(get_session), user=Depends(get_current_user)):
    part = Part(**data.dict())
    session.add(part)
    await session.commit()
    await session.refresh(part)
    return part

@router.delete("/{part_id}")
async def delete_part(part_id: int, session: AsyncSession = Depends(get_session), user=Depends(get_current_user)):
    result = await session.get(Part, part_id)
    if not result:
        raise HTTPException(status_code=404, detail="Part not found")
    await session.delete(result)
    await session.commit()
    return {"message": "Part deleted"}