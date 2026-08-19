from app.core.dependencies import get_current_user
from fastapi import APIRouter, Depends
from app.schemas.user import UserResponse, UserCreate
from app.services.user_service import UserService
# pyrefly: ignore [missing-import]
from sqlalchemy.orm import Session
from app.database.session import get_db

router = APIRouter()

@router.post("/", response_model=UserResponse)
def create_user(dados_usuario: UserCreate,
 db: Session = Depends(get_db)):
    user_service = UserService()
    novo_usuario = user_service.create_user(db=db, user=dados_usuario)

    return novo_usuario

@router.get("/me")
def get_me(current_user = Depends(get_current_user)):
   
   return current_user