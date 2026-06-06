#event-service/models.py
from sqlalchemy import Column, Integer, String, Date
from event_service.config import Base, engine
class Event(Base):
    __tablename__ = "events"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(100), nullable=False, index=True)
    city = Column(String(50), nullable=False)
    date = Column(Date, nullable=False)
    organizer = Column(String(100), nullable=False)
    organizer_email = Column(String(100), nullable=False)
Base.metadata.create_all(bind=engine)
