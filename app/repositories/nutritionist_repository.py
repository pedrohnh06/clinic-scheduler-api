from app.models.nutritionist import Nutritionist
# pyrefly: ignore [missing-import]
from sqlalchemy.orm import Session

class NutritionistRepository:

    def create(self, db: Session,
    crn: str, name: str, specialty: str, user_id: int) -> Nutritionist:

        new_nutritionist = Nutritionist(
            crn = crn,
            name = name,
            specialty = specialty,
            user_id = user_id
        )
        db.add(new_nutritionist)
        db.commit()
        db.refresh(new_nutritionist)

        return new_nutritionist

    def get_all(self, db: Session):
        return db.query(Nutritionist).all()
    
    def get_by_id(self, db: Session, nutritionist_id: int):

        search_nutritionist = db.query(
            Nutritionist
            ).filter(
                nutritionist_id == Nutritionist.id
                ).first()
        
        return search_nutritionist
    
    def update(self,
    db: Session,
    nutritionist: Nutritionist,
    update_data: dict):

        for key, value in update_data.items():
            if value is not None:
                setattr(nutritionist, key, value)
        db.commit()
        db.refresh(nutritionist)

        return nutritionist
    
    def delete(self,
    db: Session,
    nutritionist: Nutritionist):

        db.delete(nutritionist)
        db.commit()