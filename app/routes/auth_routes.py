# app/routes/auth_routes.py

from fastapi import APIRouter, Depends, HTTPException, status, Request, Response
from fastapi.security import OAuth2PasswordBearer
from fastapi.responses import JSONResponse
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from jose import JWTError
from pydantic import BaseModel, EmailStr
from models.users import User
from config import settings
from utils.db import get_async_db
from utils.errors import error_400
from utils.tokens import generate_csrf_token, create_reset_token, verify_reset_token
from utils.email import send_password_reset_email
from utils.auth import (
    verify_password,
    hash_password,
    create_access_token,
    decode_access_token,
)

router = APIRouter()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/session/login")


class LoginRequest(BaseModel):
    email: EmailStr
    password: str


@router.post("/session/login")
async def login(payload: LoginRequest, db: AsyncSession = Depends(get_async_db)):
    result = await db.execute(select(User).where(User.email == payload.email))
    user = result.scalars().first()

    print("📧 Email received:", payload.email)
    print("🔍 User found in DB:", bool(user))
    if user:
        print("🧂 Stored hash:", user.hashed_password)
        print("🔑 Password matches:", verify_password(payload.password, user.hashed_password))
        print("🧪 Comparing raw password:", payload.password)
        print("🧪 Against hash:", user.hashed_password)
        print("🧾 Rehashed password (for comparison):", hash_password(payload.password))

    if not user or not verify_password(payload.password, user.hashed_password):
        error_400("Invalid credentials")

    access_token = create_access_token({"sub": user.email})
    csrf_token = generate_csrf_token()
    secure_cookie = settings.ENVIRONMENT == "production"

    response = JSONResponse(content={
        "message": "Login successful",
        "user": {
            "id": user.id,
            "email": user.email,
            "first_name": user.first_name,
            "last_name": user.last_name,
        }
    })

    response.set_cookie(
        key="access_token",
        value=access_token,
        httponly=True,
        samesite="none",
        secure=secure_cookie
    )

    response.set_cookie(
        key="csrf_token",
        value=csrf_token,
        httponly=False,
        samesite="none",
        secure=secure_cookie
    )

    return response


async def get_current_user(request: Request, db: AsyncSession = Depends(get_async_db)) -> User:
    token = request.cookies.get("access_token")
    if not token:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Not authenticated")

    try:
        payload = decode_access_token(token)
        email: str = payload.get("sub")
        if not email:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token: missing subject")
    except JWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Could not validate credentials")

    result = await db.execute(select(User).where(User.email == email))
    user = result.scalar_one_or_none()

    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

    return user


@router.get("/session/current")
async def get_current(user: User = Depends(get_current_user)):
    return {
        "id": user.id,
        "email": user.email,
        "first_name": user.first_name,
        "last_name": user.last_name,
    }
    

@router.post("/session/logout")
async def logout():
    secure_cookie = settings.ENVIRONMENT == "production"

    response = JSONResponse(content={"message": "Logout successful"})

    response.delete_cookie(
        key="access_token",
        httponly=True,
        samesite="none",
        secure=secure_cookie
    )
    response.delete_cookie(
        key="csrf_token",
        httponly=False,
        samesite="none",
        secure=secure_cookie
    )

    return response


class PasswordResetRequest(BaseModel):
    email: EmailStr


@router.post("/session/forgot-password", status_code=status.HTTP_204_NO_CONTENT)
async def forgot_password(data: PasswordResetRequest, db: AsyncSession = Depends(get_async_db)):
    result = await db.execute(
        db.select(User).where(User.email == data.email)
    )
    user = result.scalar_one_or_none()

    if not user:
        raise HTTPException(status_code=404, detail="No user with that email")

    token = create_reset_token(user.id)
    await send_password_reset_email(user.email, token)


class PasswordReset(BaseModel):
    token: str
    new_password: str


@router.post("/session/reset-password", status_code=status.HTTP_204_NO_CONTENT)
async def reset_password(data: PasswordReset, db: AsyncSession = Depends(get_async_db)):
    user_id = verify_reset_token(data.token)

    if not user_id:
        raise HTTPException(status_code=400, detail="Invalid or expired token")

    result = await db.execute(select(User).where(User.id == user_id))
    user = result.scalar_one_or_none()

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    user.hashed_password = hash_password(data.new_password)
    await db.commit()