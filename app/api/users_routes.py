# app/api/users_routes.py

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from dependencies.auth import get_current_user
from dependencies.db import get_session
from models.users import User
from schemas.users import UserOut, PasswordUpdate
from utils.auth import get_password_hash

router = APIRouter()

# GET current user
@router.get("/me", response_model=UserOut)
async def read_current_user(current_user: User = Depends(get_current_user)):
    return current_user

# PATCH password update
@router.patch("/me/password")
async def update_password(
    data: PasswordUpdate,
    current_user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_session)
):
    if data.new_password != data.confirm_password:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Passwords do not match"
        )

    current_user.hashed_password = get_password_hash(data.new_password)
    session.add(current_user)
    await session.commit()
    return {"message": "Password updated successfully"}