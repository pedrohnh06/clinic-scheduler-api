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
                Appointment.status == status.BOOKED,
                Appointment.start_time == start_time,
                Appointment.nutritionist_id == nutritionist_id
                ).first()
            
        return existing_schedule
    
    def get_all(self, db: Session):

        return db.query(Appointment).all()