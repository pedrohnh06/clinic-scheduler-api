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