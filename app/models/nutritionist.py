# pyrefly: ignore [missing-import]
from sqlalchemy import Column, Integer, String, ForeignKey
# pyrefly: ignore [missing-import]
from sqlalchemy.orm import  relationship
from app.database.session import Base

class Nutricionista(Base):
    __tablename__ = "nutricionistas"

    id = Column(Integer, primary_key=True, index=True)
    crn = Column(String, unique=True, index=True)
    nome = Column(String, index=True)
    especialidade = Column(String, index=True)
    usuario_id = Column(Integer, ForeignKey("usuarios.id"))
    usuario = relationship("Usuario", back_populates="nutricionista")
    agendamentos = relationship("Agendamento", back_populates="nutricionista")
