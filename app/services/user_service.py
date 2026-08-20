from app.schemas.login import LoginRequest
# pyrefly: ignore [missing-import]
from sqlalchemy.orm import Session
from fastapi import HTTPException
from app.repositories.user_repository import UserRepository
from app.schemas.user import UserCreate
from app.core.security import get_password_hash, verify_password, create_access_token

class UserService:

    def __init__(self):
        self.repository = UserRepository()
    
    def create_user(self, db: Session, user: UserCreate):

        usuario_existente = self.repository.get_by_email(
            db=db, email=user.email
            )

        if usuario_existente:
            raise HTTPException(status_code=400, detail="Email já cadastrado")
        else:
            hash_gerado = get_password_hash(user.password)

        novo_usuario = self.repository.create(db=db, user_create=user,
        password_hash=hash_gerado)

        return novo_usuario

    def authenticate_user(self, user: LoginRequest, db: Session):
        buscar_usuario = self.repository.get_by_email(
            db=db, email=user.email
            )
        if not buscar_usuario:
            raise HTTPException(
                status_code=401, detail="Usuário não encontrado"
                )
        if not verify_password(user.password, buscar_usuario.password_hash):
            raise HTTPException(status_code=401, detail="Senha incorreta")
        else:
            token = create_access_token(data={"sub": buscar_usuario.email})
            return token