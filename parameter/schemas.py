from pydantic import BaseModel, EmailStr, Field
from typing import Optional


# =========================
# 🔹 TASK SCHEMAS
# =========================

class TaskCreate(BaseModel):
    title: str = Field(..., min_length=3, max_length=100)
    description: Optional[str] = None
    priority: str = Field(..., min_length=2, max_length=50)


class TaskUpdate(BaseModel):
    description: Optional[str] = None
    priority: Optional[str] = None
    status: Optional[str] = None


# =========================
# 🔹 USER SCHEMAS
# =========================

class UserCreate(BaseModel):
    name: str = Field(..., min_length=3, max_length=100)
    email: EmailStr
    password: str = Field(..., min_length=6)


class UserLogin(BaseModel):
    email: EmailStr
    password: str


# =========================
# 🔹 RESPONSE SCHEMAS (IMPORTANT)
# =========================

class UserResponse(BaseModel):
    id: int
    name: str
    email: EmailStr

    class Config:
        from_attributes = True   # for SQLAlchemy


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"