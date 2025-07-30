# app/routes/auth_routes.py

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from pydantic import BaseModel, EmailStr
from jose import JWTError, jwt
from passlib.context import CryptContext
from passlib.hash import bcrypt
from datetime import datetime, timedelta

from utils.db import get_async_db
from models.users import User
from config import settings
from utils.errors import error_400, error_401
from utils.tokens import create_reset_token, verify_reset_token
from utils.email import send_password_reset_email

router = APIRouter()
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/session/login")


class LoginRequest(BaseModel):
    email: EmailStr
    password: str


@router.post("/session/login")
async def login(payload: LoginRequest, db: AsyncSession = Depends(get_async_db)):
    """ Authenticate user and return JWT token """
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

    return {
        "message": "Login successful",
        "access_token": access_token,
        "token_type": "bearer",
        "user": {
            "id": user.id,
            "email": user.email,
            "first_name": user.first_name,
            "last_name": user.last_name,
        }
    }


@router.get("/session/current")
async def session_info_route(token: str = Depends(oauth2_scheme), db: AsyncSession = Depends(get_async_db)):
    try:
        payload = jwt.decode(token, settings.JWT_SECRET, algorithms=[settings.JWT_ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            error_401("Invalid token: missing subject")
    except JWTError:
        error_401("Could not validate credentials")

    result = await db.execute(select(User).where(User.email == email))
    user = result.scalars().first()

    if not user:
        error_401("User not found")

    return {
        "id": user.id,
        "email": user.email,
        "first_name": user.first_name,
        "last_name": user.last_name,
    }


@router.post("/session/logout")
async def logout():
    """ Frontend should remove token upon logout request """
    return {"message": "Logout successful, please remove token on client side"}


# AUTH UTILS

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def hash_password(password):
    return pwd_context.hash(password)


def create_access_token(data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=settings.JWT_EXPIRATION_MINUTES))
    to_encode.update({"exp": expire})

    print("🕒 TOKEN EXPIRES AT:", expire.isoformat())  # Debug
    return jwt.encode(to_encode, settings.JWT_SECRET, algorithm=settings.JWT_ALGORITHM)


def decode_access_token(token: str):
    try:
        payload = jwt.decode(token, settings.JWT_SECRET, algorithms=[settings.JWT_ALGORITHM])
        return payload
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid or expired token")


async def get_current_user(token: str = Depends(oauth2_scheme), db: AsyncSession = Depends(get_async_db)) -> User:
    print("🔐 TOKEN RECEIVED:", token)
    try:
        payload = jwt.decode(token, settings.JWT_SECRET, algorithms=[settings.JWT_ALGORITHM])
        print("📦 DECODED PAYLOAD:", payload)
        email: str = payload.get("sub")
        if not email:
            print("❌ No email in token!")
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token: missing subject")
    except JWTError as e:
        print("❌ JWT DECODE ERROR:", str(e))
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Could not validate credentials")

    result = await db.execute(select(User).where(User.email == email))
    user = result.scalars().first()

    if not user:
        print("❌ No user found with email:", email)
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

    print("✅ AUTHENTICATED USER:", user.email)
    return user


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

    user.hashed_password = bcrypt.hash(data.new_password)
    await db.commit()