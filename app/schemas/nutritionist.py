from pydantic import BaseModel, EmailStr, Field

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