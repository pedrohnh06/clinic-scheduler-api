# pyrefly: ignore [missing-import]
from sqlalchemy.orm import Session
from app.schemas.nutritionist import NutritionistCreate
from app.schemas.user import UserCreate
from app.repositories.nutritionist_repository import NutritionistRepository
from app.repositories.user_repository import UserRepository
from fastapi import HTTPException
from app.core.security import get_password_hash
from app.models.user import UserRole

class NutritionistService:

    def __init__(self):
        self.user_repository = UserRepository()
        self.nutritionist_repository = NutritionistRepository()

    def create_nutritionist(self,
     db: Session,
      nutritionist: NutritionistCreate):
      
    
        existing_user = self.user_repository.get_by_email(db=db, email=nutritionist.email)
        if existing_user:
            raise HTTPException(status_code=400, detail="Email já cadastrado")
        else: 
            hash_generated = get_password_hash(nutritionist.password)
        
        user_data = UserCreate(
            email=nutritionist.email,
            password=nutritionist.password,
            role=UserRole.NUTRITIONIST
        )

        new_user = self.user_repository.create(
            db=db,
            user_create=user_data,
            password_hash=hash_generated
        )

        new_nutritionist = self.nutritionist_repository.create(
            db=db,
            crn=nutritionist.crn,
            name=nutritionist.name,
            specialty=nutritionist.specialty,
            user_id=new_user.id
        )

        return new_nutritionist