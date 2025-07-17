from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.dependencies.db import get_session
from app.dependencies.auth import get_current_user
from app.models.machines import Machine
from app.schemas.machines import MachineCreate

router = APIRouter()

@router.get("/")
async def get_machines(session: AsyncSession = Depends(get_session)):
    result = await session.execute(Machine.__table__.select())
    return result.scalars().all()

@router.post("/")
async def create_machine(data: MachineCreate, session: AsyncSession = Depends(get_session), user=Depends(get_current_user)):
    machine = Machine(**data.dict())
    session.add(machine)
    await session.commit()
    await session.refresh(machine)
    return machine

@router.delete("/{machine_id}")
async def delete_machine(machine_id: int, session: AsyncSession = Depends(get_session), user=Depends(get_current_user)):
    result = await session.get(Machine, machine_id)
    if not result:
        raise HTTPException(status_code=404, detail="Machine not found")
    await session.delete(result)
    await session.commit()
    return {"message": "Machine deleted"}