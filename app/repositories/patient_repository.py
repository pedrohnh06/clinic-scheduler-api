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

    def get_all(
        self,
        db: Session,
    ):

        return db.query(Patient).all()
    
    def get_by_id(
        self,
        patient_id: int,
        db: Session
    ):

        search_patient = db.query(
            Patient
            ).filter(
                patient_id == Patient.id
                ).first()
        
        return search_patient
    
    def update_patient(
        self,
        db: Session,
        patient: Patient,
        update_data: dict
    ):

        for key, value in update_data.items():
            if value is not None:
                setattr(patient, key, value)
        db.commit()
        db.refresh(patient)

        return patient

    def delete_patient(
        self,
        db: Session,
        patient: Patient
    ):

        db.delete(patient)
        db.commit()