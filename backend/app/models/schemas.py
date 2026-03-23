from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime
from app.models.database import RoleEnum

class UserCreate(BaseModel):
    email: str
    full_name: str
    password: str
    role: RoleEnum = RoleEnum.customer
    department: Optional[str] = None

class UserOut(BaseModel):
    id: str
    email: str
    full_name: str
    role: RoleEnum
    department: Optional[str]
    is_active: bool
    created_at: datetime

    class Config:
        from_attributes = True

class LoginRequest(BaseModel):
    email: str
    password: str

class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user: UserOut

class TokenData(BaseModel):
    user_id: str
    email: str
    role: RoleEnum
    department: Optional[str] = None