from pydantic import BaseModel
from datetime import datetime
from app.models.appointment import AppointmentStatus

class AppointmentCreate(BaseModel):
    patient_id: int
    nutritionist_id: int
    start_time: datetime
    status: AppointmentStatus = AppointmentStatus.BOOKED

class AppointmentResponse(BaseModel):
    start_time: datetime
    patient_id: int
    nutritionist_id: int
    status: AppointmentStatus = AppointmentStatus.BOOKED
    id: int
    class Config:
        from_attributes = True