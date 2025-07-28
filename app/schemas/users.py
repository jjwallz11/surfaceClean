# app/schemas/users.py

from pydantic import BaseModel, EmailStr

# Base user model
class UserBase(BaseModel):
    email: EmailStr
    first_name: str
    last_name: str

# Creating a new user
class UserCreate(UserBase):
    password: str

# Returning user info
class UserOut(UserBase):
    id: int

    class Config:
        from_attributes = True

# Password update schema
class PasswordUpdate(BaseModel):
    new_password: str
    confirm_password: str