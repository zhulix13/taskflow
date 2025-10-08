# schemas.py
from pydantic import BaseModel

# ===== Task Schemas =====
class TaskBase(BaseModel):
    title: str
    description: str | None = None
    completed: bool = False

class TaskCreate(TaskBase):
    owner_id: int

class Task(TaskBase):
    id: int
    owner_id: int

    class Config:
        orm_mode = True

# ===== User Schemas =====
class UserBase(BaseModel):
    name: str
    email: str

class UserCreate(UserBase):
    password: str  # new!

class User(UserBase):
    id: int
    is_active: bool
    tasks: list[Task] = []

    class Config:
        orm_mode = True

# ===== Auth Schemas =====
class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    sub: str | None = None
