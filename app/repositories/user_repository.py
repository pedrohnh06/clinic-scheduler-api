from app.schemas.user import UserCreate
from app.models.user import User
# pyrefly: ignore [missing-import]
from sqlalchemy.orm import Session

class UserRepository:

    def get_by_email(self, db: Session, email: str) -> User | None:
        return db.query(User).filter(User.email == email).first()


    def create(self, db: Session, user_create: UserCreate, password_hash: str) -> User:
        new_user = User(
            email=user_create.email,
            password_hash=password_hash,
            role=user_create.role
        )

        db.add(new_user)
        db.commit()
        db.refresh(new_user)

        return new_user
