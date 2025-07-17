from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from utils.auth import create_access_token
from dependencies.auth import get_current_user

router = APIRouter()

@router.post("/token")
def login(form_data: OAuth2PasswordRequestForm = Depends()):
    # OAuth2PasswordRequestForm still uses .username, so treat it as email
    email = form_data.username
    password = form_data.password

    # TEMP: replace with real DB check soon
    if email != "admin@example.com" or password != "password":
        raise HTTPException(status_code=401, detail="Invalid credentials")

    access_token = create_access_token({"sub": email})
    return {"access_token": access_token, "token_type": "bearer"}

@router.get("/verify")
def verify(user: dict = Depends(get_current_user)):
    return {"user": user["sub"], "status": "token valid"}