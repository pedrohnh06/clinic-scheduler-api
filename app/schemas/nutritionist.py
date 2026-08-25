from pydantic import BaseModel, EmailStr, Field
from typing import Optional

class NutritionistResponse(BaseModel):
    id: int
    crn: str
    name: str
    specialty: str
    class Config:
        from_attributes = True

class NutritionistCreate(BaseModel):
    crn: str
    name: str
    email: EmailStr
    password: str = Field(min_length=8)
    specialty: str

class NutritionistUpdate(BaseModel):
    crn: Optional[str] = None
    name: Optional[str] = None
    password: Optional[str] = None
    specialty: Optional[str] = None
