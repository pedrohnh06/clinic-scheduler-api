from app.schemas.login import TokenResponse, LoginRequest
from fastapi import APIRouter, Depends
from app.services.user_service import UserService
# pyrefly: ignore [missing-import]
from sqlalchemy.orm import Session
from app.database.session import get_db

router = APIRouter()

@router.post("/",
 response_model=TokenResponse)
def login(dados_usuario: LoginRequest,
 db: Session = Depends(get_db)):
    user_service = UserService()
    token = user_service.authenticate_user(user=dados_usuario, db=db)

    return {"access_token": token, "token_type": "bearer"}