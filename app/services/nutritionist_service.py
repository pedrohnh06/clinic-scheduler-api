# pyrefly: ignore [missing-import]
from sqlalchemy.orm import Session
from app.schemas.nutritionist import NutritionistCreate, NutritionistUpdate
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
    nutritionist: NutritionistCreate
    ):
    
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
    
    def get_all_nutritionists(self,
    db: Session):

        search = self.nutritionist_repository.get_all(db=db)

        return search
    
    def get_by_id(self,
    db: Session,
    nutritionist_id: int):

        search = self.nutritionist_repository.get_by_id(db=db, nutritionist_id=nutritionist_id)
        if search is None:
            raise HTTPException(status_code=404, detail="Nutricionista não encontrado")
        else:
            return search
    
    def update(self,
    db: Session,
    id: int,
    nutritionist: NutritionistUpdate):

        existing_nutritionist = self.nutritionist_repository.get_by_id(db=db, nutritionist_id=id)
        if existing_nutritionist is None:
            raise HTTPException(status_code=404, detail="Nutricionista não encontrado")
        else: 
            update_data = nutritionist.model_dump(exclude_unset=True)
            update_nutritionist = self.nutritionist_repository.update(db=db, nutritionist=existing_nutritionist, update_data=update_data)

            return update_nutritionist
    
    def delete(self,
    db: Session,
    id: int):

        existing_nutritionist = self.nutritionist_repository.get_by_id(db=db, nutritionist_id=id)
        if existing_nutritionist is None:
            raise HTTPException(status_code=404, detail="Nutricionista não encontrado")
        self.nutritionist_repository.delete(db=db, nutritionist=existing_nutritionist)