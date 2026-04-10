from pydantic import BaseModel, EmailStr

class TaskCreate(BaseModel):
    title: str
    description: str | None = None
    priority: str


class TaskUpdate(BaseModel):
    description: str | None = None
    priority: str | None = None
    status: str | None = None

class UserCreate(BaseModel):
    name: str
    email: EmailStr
    password: str   

class UserLogin(BaseModel):
    email: EmailStr
    password: str    