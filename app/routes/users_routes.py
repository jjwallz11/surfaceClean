# app/api/users_routes.py

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from utils.db import get_async_db
from utils.errors import error_401, error_403, error_404
from models.users import User
from services.users_services import update_user, get_user_by_id
from schemas.users import UserResponse, UserUpdate
from utils.auth import get_current_user
from typing import List

router = APIRouter()

@router.get("", response_model=List[UserResponse])
async def get_all_users(
    db: AsyncSession = Depends(get_async_db),
    current_user: User = Depends(get_current_user)
):
    if current_user.role != "admin":
        error_401("Only admins can view all users")
    
    result = await db.execute(select(User))
    return result.scalars().all()


@router.get("/{user_id}", response_model=UserResponse)
async def get_single_user(
    user_id: int,
    db: AsyncSession = Depends(get_async_db),
    current_user: User = Depends(get_current_user)
):
    if current_user.role != "admin":
        error_401("Only admins can view other users' profiles")

    user = await get_user_by_id(db, user_id)
    if not user:
        error_404("User not found")
    return user


@router.put("/{user_id}", response_model=UserResponse)
async def update_user_route(
    user_id: int,
    user: UserUpdate,
    db: AsyncSession = Depends(get_async_db),
    current_user: User = Depends(get_current_user)
):
    if current_user.id != user_id:
        error_403("You can only update your own profile")

    db_user = await get_user_by_id(db, user_id)
    if not db_user:
        error_404("User not found")

    updated_user = await update_user(db, db_user, user)
    return updated_user