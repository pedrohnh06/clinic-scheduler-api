from app.services.patient_service import PatientService
from app.database.session import get_db
# pyrefly: ignore [missing-import]
from sqlalchemy.orm import Session
from app.schemas.patient import PatientCreate, PatientResponse
from fastapi import APIRouter, Depends

router = APIRouter()

@router.post("/", response_model=PatientResponse)
def create_patient(data: PatientCreate, db: Session = Depends(get_db)):
    patient_service = PatientService()
    new_patient = patient_service.create_patient(db=db, patient=data)

    return new_patient