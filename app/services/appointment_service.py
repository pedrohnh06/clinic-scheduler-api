# pyrefly: ignore [missing-import]
from sqlalchemy.orm import Session
from app.schemas.appointment import AppointmentCreate
from app.repositories.appointment_repository import AppointmentRepository
from fastapi import HTTPException
from datetime import datetime, timezone

class AppointmentService:

    def __init__(self):
        self.appointment_repository = AppointmentRepository()

    def create_appoint(
        self,
        db: Session,
        appointment: AppointmentCreate
        ):

        check_date = appointment.start_time < datetime.now(timezone.utc)
        if check_date == True:
            raise HTTPException(status_code=400, detail="A data do agendamento não pode estar no passado")
        else: 
            existing_date = self.appointment_repository.check_conflict(
                status=appointment.status,
                nutritionist_id=appointment.nutritionist_id,
                start_time=appointment.start_time, db=db
            )
            if existing_date:
                raise HTTPException(status_code=400, detail="Horário já reservado para este nutricionista")
            else:
                new_appointment = self.appointment_repository.create(
                    patient_id=appointment.patient_id,
                    nutritionist_id=appointment.nutritionist_id,
                    start_time=appointment.start_time,
                    status=appointment.status,
                    db=db
                )
            
            return new_appointment

    def get_all_appointment(
        self,
        db: Session
    ):

        search = self.appointment_repository.get_all(db)

        return search