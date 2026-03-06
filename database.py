from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from models import Base

# SQLite database for production and development
DATABASE_URL = "sqlite:///./printing_shop.db"

engine = create_engine(
    DATABASE_URL, connect_args={"check_same_thread": False}
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create tables if they don't exist
Base.metadata.create_all(bind=engine)

# Dependency for FastAPI routes

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()