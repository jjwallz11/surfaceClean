# app/api/auth_routes.py
from fastapi import APIRouter, Depends
from app.dependencies.auth import get_current_user
from app.models.users import User

router = APIRouter()

@router.get("/me")
def read_current_user(current_user: User = Depends(get_current_user)):
    return current_user