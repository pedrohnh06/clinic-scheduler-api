from pydantic import BaseModel, EmailStr, Field
from app.models.user import UserRole

class UserResponse(BaseModel):
    id: int
    email: str
    class Config:
        from_attributes = True

class UserCreate(BaseModel):
    email: EmailStr
    password: str = Field(min_length=8)
    role: UserRole
