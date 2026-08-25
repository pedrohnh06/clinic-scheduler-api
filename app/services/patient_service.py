# pyrefly: ignore [missing-import]
from sqlalchemy.orm import Session
from app.schemas.patient import PatientCreate, PatientUpdate
from app.schemas.user import UserCreate
from app.repositories.patient_repository import PatientRepository
from app.repositories.user_repository import UserRepository
from fastapi import HTTPException
from app.core.security import get_password_hash
from app.models.user import UserRole

class PatientService:

    def __init__(self):
        self.user_repository = UserRepository()
        self.patient_repository = PatientRepository()

    def create_patient(self, db: Session, patient: PatientCreate):

        existing_patient = self.user_repository.get_by_email(
            db=db, email=patient.email
            )
        if existing_patient:
            raise HTTPException(status_code=400, detail="Email já cadastrado")
        else: 
            hash_generated = get_password_hash(patient.password)

        user_data = UserCreate(
            email=patient.email,
            password=patient.password,
            role=UserRole.PATIENT
        )

        new_user = self.user_repository.create(
            db=db,
            user_create=user_data,
            password_hash=hash_generated)

        new_patient = self.patient_repository.create(db=db,
        name=patient.name,
        birth_date=patient.birth_date,
        user_id=new_user.id)

        return new_patient
    
    def get_all_patients(
        self,
        db: Session,
    ):
        patient_repository = PatientRepository()
        get_all_patients = patient_repository.get_all(db=db)

        return get_all_patients
    
    def get_by_id_patient(
        self,
        db: Session,
        patient_id: int
    ):
        search = self.patient_repository.get_by_id(patient_id=patient_id, db=db)
        if search is None:
            raise HTTPException(status_code=404, detail="Paciente não encontrado")
        else:
            return search
    
    def update_patient(
        self,
        db: Session,
        patient_id: int,
        patient: PatientUpdate
    ):

        existing_patient = self.patient_repository.get_by_id(patient_id=patient_id, db=db)
        if existing_patient is None:
            raise HTTPException(status_code=404, detail="Paciente não encontrado")
        else:
            update_data = patient.model_dump(exclude_unset=True)
            update_patient = self.patient_repository.update_patient(
                db=db,
                patient=existing_patient,
                update_data=update_data
            )

            return update_patient
    
    def delete_patient(
        self,
        db: Session,
        patient_id: int
    ):

        existing_patient = self.patient_repository.get_by_id(patient_id=patient_id, db=db)
        if existing_patient is None:
            raise HTTPException(status_code=404, detail="Paciente não encontrado")
        else:
            self.patient_repository.delete_patient(db=db, patient=existing_patient)

        