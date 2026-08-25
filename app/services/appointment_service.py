# pyrefly: ignore [missing-import]
from sqlalchemy.orm import Session
from app.schemas.appointment import AppointmentCreate, AppointmentUpdate
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
        db: Session,
        nutritionist_id=None,
        patient_id=None
    ):

        search = self.appointment_repository.get_all(db, nutritionist_id, patient_id)

        return search
    
    def appointment_update(
        self,
        db: Session,
        id: int,
        appointment: AppointmentUpdate
    ):  

        existing_appointment = self.appointment_repository.get_by_id(
            db=db,
            appointment_id=id
        )

        if existing_appointment:
            if appointment.start_time is not None:
                check_date = appointment.start_time < datetime.now(timezone.utc)
                if check_date == True:
                    raise HTTPException(status_code=400, detail="Você não pode agendar um horário no passado")
                else:
                    nutritionist_to_check = appointment.nutritionist_id or existing_appointment.nutritionist_id
                    status_to_check = appointment.status or existing_appointment.status
                    existing_date = self.appointment_repository.check_conflict(
                        status=status_to_check,
                        nutritionist_id=nutritionist_to_check,
                        start_time=appointment.start_time,
                        db=db
                        )
                    if existing_date:
                        raise HTTPException(status_code=400, detail="Esse horário já está agendado")
                    else:
                        update_data = appointment.model_dump(exclude_unset=True)
                        update_appointment = self.appointment_repository.update(
                            db=db,
                            appointment=existing_appointment,
                            update_data=update_data
                        )

                        return update_appointment
        else:
            raise HTTPException(status_code=404, detail="Agendamento não encontrado")

    def appointment_delete(self,
        db: Session,
        id: int
    ):

        existing_appointment = self.appointment_repository.get_by_id(
            db=db,
            appointment_id=id
        )
        if existing_appointment is None:
            raise HTTPException(status_code=404, detail="O agendamento não existe")
        
        self.appointment_repository.delete(db=db, appointment=existing_appointment)