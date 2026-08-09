# pyrefly: ignore [missing-import]
from sqlalchemy import Column, Integer, String, Enum
# pyrefly: ignore [missing-import]
from sqlalchemy.orm import relationship
from app.database.session import Base
import enum

class UserRole(enum.Enum):
    PATIENT = "patient"
    NUTRITIONIST = "nutritionist"
    ADMIN = "admin"

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    password_hash = Column(String)
    role = Column(Enum(UserRole))
    
    nutritionist = relationship("Nutritionist", back_populates="user", uselist=False)
    patient = relationship("Patient", back_populates="user", uselist=False)