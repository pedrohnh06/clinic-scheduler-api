from app.database.session import get_db
from fastapi import Depends, HTTPException
from jose import jwt, JWTError
from fastapi.security import OAuth2PasswordBearer
from app.core.security import SECRET_KEY, ALGORITHM
from app.repositories.user_repository import UserRepository
# pyrefly: ignore [missing-import]
from sqlalchemy.orm import Session

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")
repository = UserRepository()

def get_current_user(token: str = Depends(oauth2_scheme),
 db: Session = Depends(get_db),
 ):

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")

        if email is None:
            raise HTTPException(status_code=401, detail="Token Inválido")
        usuario = repository.get_by_email(db=db, email=email)
        if usuario is None: 
            raise HTTPException(status_code=401, detail="Usuário não encontrado")

        return usuario

    except JWTError:
        raise HTTPException(status_code=401, detail="Pulseira falsa ou vencida")