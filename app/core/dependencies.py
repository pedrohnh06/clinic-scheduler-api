from app.models.user import UserRole
from app.database.session import get_db
from fastapi import Depends, HTTPException
from jose import jwt, JWTError
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from app.core.security import SECRET_KEY, ALGORITHM
from app.repositories.user_repository import UserRepository
# pyrefly: ignore [missing-import]
from sqlalchemy.orm import Session
from app.models.nutritionist import Nutritionist
from app.models.patient import Patient
from app.models.user import User

security = HTTPBearer()

repository = UserRepository()

def get_current_user(
credentials: HTTPAuthorizationCredentials = Depends(security),
db: Session = Depends(get_db),
):

    token = credentials.credentials

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")

        if email is None:
            raise HTTPException(status_code=401, detail="Token Inválido")
        user = repository.get_by_email(db=db, email=email)
        if user is None: 
            raise HTTPException(status_code=401, detail="Usuário não encontrado")

        return user

    except JWTError:
        raise HTTPException(status_code=401, detail="Pulseira falsa ou vencida")

def get_current_profile(
credentials: HTTPAuthorizationCredentials = Depends(security),
db: Session = Depends(get_db)):

    logged_user = get_current_user(credentials, db=db)

    if logged_user.role == UserRole.NUTRITIONIST:
        profile = db.query(Nutritionist).filter(
            Nutritionist.user_id == logged_user.id
        ).first()
        return {"role": "NUTRITIONIST",
        "profile_id": profile.id}

    if logged_user.role == UserRole.PATIENT:
        profile = db.query(Patient).filter(
            Patient.user_id == logged_user.id
        ).first()
        return {"role": "PATIENT",
        "profile_id": profile.id}