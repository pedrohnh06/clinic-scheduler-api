# pyrefly: ignore [missing-import]
from sqlalchemy.orm import Session
from app.models.patient import Patient
from datetime import date

class PatientRepository:

    def create(self,
     db: Session,
     name: str,
     birth_date: date,
     user_id: int) -> Patient:

        new_patient = Patient(
            name = name,
            birth_date = birth_date,
            user_id = user_id
        )

        db.add(new_patient)
        db.commit()
        db.refresh(new_patient)

        return new_patient