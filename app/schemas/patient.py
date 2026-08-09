from datetime import date
from pydantic import BaseModel, EmailStr, Field

class PatientResponse(BaseModel):
    id: int
    name: str
    birth_date: date
    class Config:
        from_attributes = True

class PatientCreate(BaseModel):
    name: str
    birth_date: date
    email: EmailStr
    password: str = Field(min_length=8)