# pyrefly: ignore [missing-import]
from sqlalchemy import Column, Integer, ForeignKey, DateTime, Enum
# pyrefly: ignore [missing-import]
from sqlalchemy.orm import  relationship
from app.database.session import Base
import enum

class AppointmentStatus(enum.Enum):
    OCUPADO = "ocupado"
    BLOQUEADO = "bloqueado"

class Agendamento(Base):
    __tablename__ = "agendamentos"

    id = Column(Integer, primary_key=True, index=True)
    data_hora_inicio = Column(DateTime)
    id_nutricionista = Column(Integer, ForeignKey("nutricionistas.id"))
    id_paciente = Column(Integer, ForeignKey("pacientes.id"), nullable=True)
    status = Column(Enum(AppointmentStatus))
    nutricionista = relationship("Nutricionista", back_populates="agendamentos", uselist=False)
    paciente = relationship("Paciente", back_populates="agendamentos", uselist=False)

