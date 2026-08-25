from typing import Optional
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
    patient_id: Optional[int] = None
    nutritionist_id: Optional[int] = None
    status: AppointmentStatus = AppointmentStatus.BOOKED
    id: int
    class Config:
        from_attributes = True

class AppointmentUpdate(BaseModel):
    start_time: Optional[datetime] = None
    patient_id: Optional[int] = None
    nutritionist_id: Optional[int] = None
    status: Optional[AppointmentStatus] = None