# app/api/machines_routes.py

from fastapi import APIRouter, Depends, HTTPException, Path
from sqlalchemy.orm import Session
from sqlalchemy import select
from app.dependencies.db import get_db
from app.dependencies.auth import get_current_user
from app.models.machines import Machine
from app.schemas.machines import MachineCreate, MachineUpdate

router = APIRouter()

# READ
@router.get("/")
def get_machines(session: Session = Depends(get_db)):
    result = session.execute(select(Machine))
    return result.scalars().all()

# CREATE
@router.post("/")
def create_machine(
    data: MachineCreate,
    session: Session = Depends(get_db),
    user=Depends(get_current_user)
):
    machine = Machine(**data.dict())
    session.add(machine)
    session.commit()
    session.refresh(machine)
    return machine

# UPDATE
@router.put("/{machine_id}")
def update_machine(
    machine_id: int = Path(..., gt=0),
    data: MachineUpdate = Depends(),
    session: Session = Depends(get_db),
    user=Depends(get_current_user)
):
    machine = session.get(Machine, machine_id)
    if not machine:
        raise HTTPException(status_code=404, detail="Machine not found")
    
    for key, value in data.dict(exclude_unset=True).items():
        setattr(machine, key, value)

    session.commit()
    session.refresh(machine)
    return machine

# DELETE
@router.delete("/{machine_id}")
def delete_machine(
    machine_id: int,
    session: Session = Depends(get_db),
    user=Depends(get_current_user)
):
    machine = session.get(Machine, machine_id)
    if not machine:
        raise HTTPException(status_code=404, detail="Machine not found")
    session.delete(machine)
    session.commit()
    return {"message": "Machine deleted"}