# pyrefly: ignore [missing-import]
from sqlalchemy import Column, Integer, String, ForeignKey, Date
# pyrefly: ignore [missing-import]
from sqlalchemy.orm import  relationship
from app.database.session import Base

class Paciente(Base):
    __tablename__ = "pacientes"

    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String, index=True)
    data_nascimento = Column(Date)
    usuario_id = Column(Integer, ForeignKey("usuarios.id"))
    usuario = relationship("Usuario", back_populates="paciente")
    agendamentos = relationship("Agendamento", back_populates="paciente")