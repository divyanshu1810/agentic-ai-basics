# event_service/config.py
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
DATABASE_URL = "sqlite:///events.db"
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
session = sessionmaker(bind=engine)
Base = declarative_base()
# Dependency: Get DB session
def get_db():
    db = session()
    try:
        yield db
    finally:
        db.close()
