from fastapi import FastAPI
from app.api.user_router import router as user_router
from app.api.auth_router import router as auth_router
from app.api.nutritionist_router import router as nutritionist_router
from app.api.patient_router import router as patient_router
from app.api.appointment_router import router as appointment_router
import app.models 

app = FastAPI()

app.include_router(user_router, prefix="/users", tags=["Users"])
app.include_router(auth_router, prefix="/login", tags=["Auth"])
app.include_router(nutritionist_router, prefix="/nutritionists", tags=["Nutritionists"])
app.include_router(patient_router, prefix="/patients", tags=["Patients"])
app.include_router(appointment_router, prefix="/appointment", tags=["Appointments"])