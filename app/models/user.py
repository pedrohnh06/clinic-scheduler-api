# pyrefly: ignore [missing-import]
from sqlalchemy import Column, Integer, String, Enum
# pyrefly: ignore [missing-import]
from sqlalchemy.orm import  relationship
from app.database.session import Base
import enum

class UserRole(enum.Enum):
    PACIENTE = "paciente"
    NUTRICIONISTA = "nutricionista"
    ADMIN = "admin"

class Usuario(Base):
    __tablename__ = "usuarios"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    senha_hash = Column(String)
    tipo_usuario = Column(Enum(UserRole))
    nutricionista = relationship("Nutricionista", back_populates="usuario", uselist=False)
    paciente = relationship("Paciente", back_populates="usuario", uselist=False)