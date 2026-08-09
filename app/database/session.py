# pyrefly: ignore [missing-import]
from sqlalchemy import create_engine
# pyrefly: ignore [missing-import]
from sqlalchemy.orm import sessionmaker, declarative_base
import os
# pyrefly: ignore [missing-import]
from dotenv import load_dotenv

load_dotenv()

DATA_BASE_URL = os.getenv("DATABASE_URL", "sqlite:///./agendamentos.db")

if DATA_BASE_URL.startswith("sqlite"):
    engine = create_engine(DATA_BASE_URL, connect_args={"check_same_thread": False})
else:
    engine = create_engine(DATA_BASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()