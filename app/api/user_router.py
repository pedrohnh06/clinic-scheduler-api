from app.core.dependencies import get_current_user, get_current_profile
from fastapi import APIRouter, Depends
from app.schemas.user import UserResponse, UserCreate
from app.services.user_service import UserService
# pyrefly: ignore [missing-import]
from sqlalchemy.orm import Session
from app.database.session import get_db

router = APIRouter()

@router.post("/", response_model=UserResponse)
def create_user(data_user: UserCreate,
 db: Session = Depends(get_db)):
    user_service = UserService()
    new_user = user_service.create_user(db=db, user=data_user)

    return new_user

@router.get("/me")
def get_me(current_profile = Depends(get_current_profile)):
   
   return current_profile