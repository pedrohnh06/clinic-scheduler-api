from fastapi import FastAPI
from app.api.user_router import router as user_router
from app.api.auth_router import router as auth_router
import app.models 

app = FastAPI()

app.include_router(user_router, prefix="/users", tags=["Users"])
app.include_router(auth_router, prefix="/login", tags=["Login"])