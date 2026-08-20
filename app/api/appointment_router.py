from app.services.appointment_service import AppointmentService
from app.database.session import get_db
from fastapi import APIRouter, Depends
from app.schemas.appointment import AppointmentCreate, AppointmentResponse
# pyrefly: ignore [missing-import]
from sqlalchemy.orm import Session
from app.core.dependencies import get_current_user
from app.models.appointment import Appointment

router = APIRouter()

@router.post("/", response_model = AppointmentResponse)
def create_appointment(
    data: AppointmentCreate,
    logged_user = Depends(get_current_user),
    db: Session = Depends(get_db)):

    appointment_service = AppointmentService()
    new_appointment = appointment_service.create_appoint(db=db, appointment=data)

    return new_appointment