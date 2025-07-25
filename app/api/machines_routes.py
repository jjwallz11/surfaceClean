# app/api/machines_routes.py

from fastapi import APIRouter, Depends, HTTPException, Path
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from dependencies.db import get_session
from dependencies.auth import get_current_user
from models.machines import Machine
from schemas.machines import MachineCreate, MachineUpdate

router = APIRouter()

# READ
@router.get("/")
async def get_machines(session: AsyncSession = Depends(get_session)):
    result = await session.execute(select(Machine))
    return result.scalars().all()

# CREATE
@router.post("/")
async def create_machine(
    data: MachineCreate,
    session: AsyncSession = Depends(get_session),
    user=Depends(get_current_user)
):
    machine = Machine(**data.dict())
    session.add(machine)
    await session.commit()
    await session.refresh(machine)
    return machine

# UPDATE
@router.put("/{machine_id}")
async def update_machine(
    machine_id: int = Path(..., gt=0),
    data: MachineUpdate = Depends(),
    session: AsyncSession = Depends(get_session),
    user=Depends(get_current_user)
):
    machine = await session.get(Machine, machine_id)
    if not machine:
        raise HTTPException(status_code=404, detail="Machine not found")
    
    for key, value in data.dict(exclude_unset=True).items():
        setattr(machine, key, value)

    await session.commit()
    await session.refresh(machine)
    return machine

# DELETE
@router.delete("/{machine_id}")
async def delete_machine(
    machine_id: int,
    session: AsyncSession = Depends(get_session),
    user=Depends(get_current_user)
):
    machine = await session.get(Machine, machine_id)
    if not machine:
        raise HTTPException(status_code=404, detail="Machine not found")
    await session.delete(machine)
    await session.commit()
    return {"message": "Machine deleted"}