from typing import Optional
from app.services.appointment_service import AppointmentService
from app.database.session import get_db
from fastapi import APIRouter, Depends
from app.schemas.appointment import AppointmentCreate, AppointmentResponse, AppointmentUpdate
# pyrefly: ignore [missing-import]
from sqlalchemy.orm import Session
from app.core.dependencies import get_current_user
router = APIRouter()

@router.post("/", response_model = AppointmentResponse)
def create_appointment(
    data: AppointmentCreate,
    logged_user = Depends(get_current_user),
    db: Session = Depends(get_db)
):

    appointment_service = AppointmentService()
    new_appointment = appointment_service.create_appoint(db=db, appointment=data)

    return new_appointment

@router.get("/", response_model = list[AppointmentResponse])
def appointment_get_all(
    db: Session = Depends(get_db),
    logged_user = Depends(get_current_user),
    nutritionist_id: Optional[int] = None,
    patient_id: Optional[int] = None
):

    appointment_service = AppointmentService()
    appointment_get = appointment_service.get_all_appointment(
        db=db,
        nutritionist_id=nutritionist_id,
        patient_id=patient_id)
    return appointment_get

@router.put("/{appointment_id}", response_model = AppointmentResponse)
def appointment_update(
    appointment_id: int,
    appointment: AppointmentUpdate,
    db: Session = Depends(get_db),
    logged_user = Depends(get_current_user)
):

    appointment_service = AppointmentService()
    appointment_update = appointment_service.appointment_update(db=db,
    id=appointment_id,
    appointment=appointment)

    return appointment_update

@router.delete("/{appointment_id}")
def appointment_delete(
    appointment_id: int,
    db: Session = Depends(get_db),
    logged_user = Depends(get_current_user),
):

    appointment_service = AppointmentService()
    appointment_delete = appointment_service.appointment_delete(
        db=db,
        id=appointment_id
        )

    return appointment_delete