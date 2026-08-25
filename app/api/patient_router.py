from app.core.dependencies import get_current_user
from app.services.patient_service import PatientService
from app.database.session import get_db
# pyrefly: ignore [missing-import]
from sqlalchemy.orm import Session
from app.schemas.patient import PatientCreate, PatientResponse, PatientUpdate
from fastapi import APIRouter, Depends

router = APIRouter()

@router.post("/", response_model=PatientResponse)
def create_patient(data: PatientCreate, db: Session = Depends(get_db)):
    patient_service = PatientService()
    new_patient = patient_service.create_patient(db=db, patient=data)

    return new_patient

@router.get("/", response_model=list[PatientResponse])
def get_all_patients(
    db: Session = Depends(get_db),
    logged_user = Depends(get_current_user)
):

    patient_service = PatientService()
    get_all = patient_service.get_all_patients(db=db)

    return get_all

@router.get("/{patient_id}", response_model=PatientResponse)
def get_by_id_patient(
    patient_id: int,
    db: Session = Depends(get_db),
    logged_user = Depends(get_current_user)
):

    patient_service = PatientService()
    get_by_id_patient = patient_service.get_by_id_patient(db=db, patient_id=patient_id)

    return get_by_id_patient

@router.put("/{patient_id}", response_model=PatientResponse)
def update_patient(
    patient_id: int,
    patient: PatientUpdate,
    db: Session = Depends(get_db),
    logged_user = Depends(get_current_user)
):

    patient_service = PatientService()
    update_patient = patient_service.update_patient(db=db, patient_id=patient_id, patient=patient)

    return update_patient

@router.delete("/{patient_id}")
def delete_patient(
    patient_id: int,
    db: Session = Depends(get_db),
    logged_user = Depends(get_current_user)
):

    patient_service = PatientService()
    delete_patient = patient_service.delete_patient(db=db, patient_id=patient_id)

    return delete_patient