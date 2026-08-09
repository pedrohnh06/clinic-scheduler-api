# pyrefly: ignore [missing-import]
from sqlalchemy import Column, Integer, String, ForeignKey, Date
# pyrefly: ignore [missing-import]
from sqlalchemy.orm import relationship
from app.database.session import Base

class Patient(Base):
    __tablename__ = "patients"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    birth_date = Column(Date)
    user_id = Column(Integer, ForeignKey("users.id"))
    
    user = relationship("User", back_populates="patient")
    appointments = relationship("Appointment", back_populates="patient")