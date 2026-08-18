from datetime import datetime, timedelta, timezone
from jose import jwt 
# pyrefly: ignore [missing-import]
from passlib.context import CryptContext
import os

ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "30"))
SECRET_KEY = os.getenv("SECRET_KEY", "uma-chave-temporaria-trocar-em-producao")
ALGORITHM = os.getenv("ALGORITHM", "HS256")

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def create_access_token(data: dict):
    to_encode = data.copy()

    expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp":expire})

    token_jwt = jwt.encode(to_encode ,SECRET_KEY, algorithm=ALGORITHM)

    return token_jwt

def verify_password(plain_password, hashed_password) -> bool:
     return  pwd_context.verify(plain_password,hashed_password)

def get_password_hash(password: str) -> str:
        return pwd_context.hash(password)
    
