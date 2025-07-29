# app/api/machines_routes.py

from fastapi import APIRouter, Depends, HTTPException, Path
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from utils.db import get_async_db
from utils.auth import get_current_user
from models.machines import Machine
from schemas.machines import MachineCreate, MachineUpdate
from typing import List

router = APIRouter()

# READ
@router.get("/", response_model=List[MachineCreate])
async def get_machines(
    db: AsyncSession = Depends(get_async_db)
):
    result = await db.execute(select(Machine))
    return result.scalars().all()

# CREATE
@router.post("/", response_model=MachineCreate)
async def create_machine(
    data: MachineCreate,
    db: AsyncSession = Depends(get_async_db),
    user=Depends(get_current_user)
):
    machine = Machine(**data.dict())
    db.add(machine)
    await db.commit()
    await db.refresh(machine)
    return machine

# UPDATE
@router.put("/{machine_id}", response_model=MachineCreate)
async def update_machine(
    machine_id: int = Path(..., gt=0),
    data: MachineUpdate = Depends(),
    db: AsyncSession = Depends(get_async_db),
    user=Depends(get_current_user)
):
    result = await db.execute(select(Machine).where(Machine.id == machine_id))
    machine = result.scalar_one_or_none()

    if not machine:
        raise HTTPException(status_code=404, detail="Machine not found")

    for key, value in data.dict(exclude_unset=True).items():
        setattr(machine, key, value)

    await db.commit()
    await db.refresh(machine)
    return machine

# DELETE
@router.delete("/{machine_id}")
async def delete_machine(
    machine_id: int,
    db: AsyncSession = Depends(get_async_db),
    user=Depends(get_current_user)
):
    result = await db.execute(select(Machine).where(Machine.id == machine_id))
    machine = result.scalar_one_or_none()

    if not machine:
        raise HTTPException(status_code=404, detail="Machine not found")

    await db.delete(machine)
    await db.commit()
    return {"message": "Machine deleted"}