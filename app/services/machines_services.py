# app/services/machines_services.py

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from models.machines import Machine
from schemas.machines import MachineCreate, MachineUpdate
from typing import Optional

async def create_machine(db: AsyncSession, machine_data: MachineCreate) -> Machine:
    machine = Machine(**machine_data.dict())
    db.add(machine)
    await db.commit()
    await db.refresh(machine)
    return machine

async def get_all_machines(db: AsyncSession) -> list[Machine]:
    result = await db.execute(select(Machine))
    return result.scalars().all()

async def update_machine(
    db: AsyncSession,
    machine_id: int,
    machine_data: MachineUpdate
) -> Optional[Machine]:
    result = await db.execute(select(Machine).where(Machine.id == machine_id))
    machine = result.scalar_one_or_none()
    if not machine:
        return None

    for key, value in machine_data.dict(exclude_unset=True).items():
        setattr(machine, key, value)

    await db.commit()
    await db.refresh(machine)
    return machine

async def delete_machine(db: AsyncSession, machine_id: int) -> Optional[Machine]:
    result = await db.execute(select(Machine).where(Machine.id == machine_id))
    machine = result.scalar_one_or_none()
    if not machine:
        return None

    await db.delete(machine)
    await db.commit()
    return machine