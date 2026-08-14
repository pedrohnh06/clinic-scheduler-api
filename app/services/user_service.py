# pyrefly: ignore [missing-import]
from sqlalchemy.orm import Session
# pyrefly: ignore [missing-import]
from passlib.context import CryptContext
from fastapi import HTTPException
from app.repositories.user_repository import UserRepository
from app.schemas.user import UserCreate

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class UserService:

    def __init__(self):
        self.repository = UserRepository()

    def get_password_hash(self, password: str) -> str:
        return pwd_context.hash(password)
    
    def create_user(self, db: Session, user: UserCreate):

        usuario_existente = self.repository.get_by_email(
            db=db, email=user.email
            )

        if usuario_existente:
            raise HTTPException(status_code=400, detail="Email já cadastrado")
        else:
            hash_gerado = self.get_password_hash(user.password)

        novo_usuario = self.repository.create(db=db, user_create=user,
        password_hash=hash_gerado)

        return novo_usuario