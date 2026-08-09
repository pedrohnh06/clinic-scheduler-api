# pyrefly: ignore [missing-import]
from sqlalchemy import Column, Integer, String, ForeignKey
# pyrefly: ignore [missing-import]
from sqlalchemy.orm import relationship
from app.database.session import Base

class Nutritionist(Base):
    __tablename__ = "nutritionists"

    id = Column(Integer, primary_key=True, index=True)
    crn = Column(String, unique=True, index=True)
    name = Column(String, index=True)
    specialty = Column(String, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    
    user = relationship("User", back_populates="nutritionist")
    appointments = relationship("Appointment", back_populates="nutritionist")
