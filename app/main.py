from fastapi import FastAPI
from app.api.user_router import router
import app.models 

app = FastAPI()

app.include_router(router, prefix="/users", tags=["Users"])