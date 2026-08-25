from app.services.nutritionist_service import NutritionistService
from app.database.session import get_db
# pyrefly: ignore [missing-import]
from sqlalchemy.orm import Session
from app.schemas.nutritionist import NutritionistCreate, NutritionistResponse, NutritionistUpdate
from fastapi import APIRouter, Depends
from app.core.dependencies import get_current_user

router = APIRouter()

@router.post("/", response_model=NutritionistResponse)
def create_nutritionist(data: NutritionistCreate,
db: Session = Depends(get_db)):
    nutritionist_service = NutritionistService()
    new_nutritionist = nutritionist_service.create_nutritionist(db=db, nutritionist=data)

    return new_nutritionist

@router.get("/", response_model=list[NutritionistResponse])
def get_all(
db: Session = Depends(get_db),
logged_user = Depends(get_current_user)):

    nutritionist_service = NutritionistService()
    nutritionist_get = nutritionist_service.get_all_nutritionists(db=db)

    return nutritionist_get

@router.get("/{nutritionist_id}", response_model=NutritionistResponse)
def get_by_id(
nutritionist_id: int,
db: Session = Depends(get_db),
logged_user = Depends(get_current_user)):

    nutritionist_service = NutritionistService()
    nutritionist_get_by_id = nutritionist_service.get_by_id(db=db, nutritionist_id=nutritionist_id)

    return nutritionist_get_by_id

@router.put("/{nutritionist_id}", response_model=NutritionistResponse)
def update_nutritionist(
nutritionist_id: int,
nutritionist: NutritionistUpdate,
db: Session = Depends(get_db),
logged_user = Depends(get_current_user)):

    nutritionist_service = NutritionistService()
    update_nutritionist = nutritionist_service.update(db=db, id=nutritionist_id, nutritionist=nutritionist)

    return update_nutritionist

@router.delete("/{nutritionist_id}")
def delete_nutritionist(
    nutritionist_id: int,
    db: Session = Depends(get_db),
    logged_user = Depends(get_current_user)
):

    nutritionist_service = NutritionistService()
    delete_nutritionist = nutritionist_service.delete(db=db, id=nutritionist_id)

    return delete_nutritionist