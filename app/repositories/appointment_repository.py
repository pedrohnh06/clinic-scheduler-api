# pyrefly: ignore [missing-import]
from sqlalchemy.orm import Session
from app.models.appointment import Appointment, AppointmentStatus
from datetime import datetime
class AppointmentRepository:

    def create(
        self, patient_id: int,
        nutritionist_id: int,
        start_time: datetime,
        status: AppointmentStatus,
        db: Session
        ) -> Appointment:

        new_appointment = Appointment(
            patient_id = patient_id,
            nutritionist_id = nutritionist_id,
            start_time = start_time,
            status = status
        )

        db.add(new_appointment)
        db.commit()
        db.refresh(new_appointment)

        return new_appointment

    def check_conflict(
        self,
        status: AppointmentStatus,
        nutritionist_id: int,
        start_time: datetime,
        db: Session):

        existing_schedule = db.query(
            Appointment
            ).filter(
                Appointment.status == AppointmentStatus.BOOKED,
                Appointment.start_time == start_time,
                Appointment.nutritionist_id == nutritionist_id
                ).first()
            
        return existing_schedule
    
    def get_all(
        self,
        db: Session,
        nutritionist_id=None,
        patient_id=None):

        query = db.query(Appointment)
        if nutritionist_id is not None: 
            query = query.filter(Appointment.nutritionist_id == nutritionist_id)
        if patient_id is not None:
            query = query.filter(Appointment.patient_id == patient_id)

        return query.all()

    def get_by_id(
        self,
        db: Session,
        appointment_id: int
    ):

        search_appointment = db.query(
            Appointment
            ).filter(
                appointment_id == Appointment.id,
                ).first()
            
        return search_appointment
    
    def update(
        self,
        db: Session,
        appointment: Appointment,
        update_data: dict
    ):
        for key, value in update_data.items():
            if value is not None:
                setattr(appointment, key, value)
        db.commit()
        db.refresh(appointment)

        return appointment

    def delete(
        self,
        db: Session,
        appointment: Appointment
    ):

        db.delete(appointment)
        db.commit()