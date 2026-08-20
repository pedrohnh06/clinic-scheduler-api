from app.services.nutritionist_service import NutritionistService
from app.database.session import get_db
# pyrefly: ignore [missing-import]
from sqlalchemy.orm import Session
from app.schemas.nutritionist import NutritionistCreate, NutritionistResponse
from fastapi import APIRouter, Depends

router = APIRouter()

@router.post("/", response_model=NutritionistResponse)
def create_nutritionist(data: NutritionistCreate,
db: Session = Depends(get_db)):
    nutritionist_service = NutritionistService()
    new_nutritionist = nutritionist_service.create_nutritionist(db=db, nutritionist=data)

    return new_nutritionist