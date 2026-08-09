# pyrefly: ignore [missing-import]
from sqlalchemy import Column, Integer, ForeignKey, DateTime, Enum
# pyrefly: ignore [missing-import]
from sqlalchemy.orm import relationship
from app.database.session import Base
import enum

class AppointmentStatus(enum.Enum):
    BOOKED = "booked"
    BLOCKED = "blocked"

class Appointment(Base):
    __tablename__ = "appointments"

    id = Column(Integer, primary_key=True, index=True)
    start_time = Column(DateTime)
    nutritionist_id = Column(Integer, ForeignKey("nutritionists.id"))
    patient_id = Column(Integer, ForeignKey("patients.id"), nullable=True)
    status = Column(Enum(AppointmentStatus))
    
    nutritionist = relationship("Nutritionist", back_populates="appointments", uselist=False)
    patient = relationship("Patient", back_populates="appointments", uselist=False)
