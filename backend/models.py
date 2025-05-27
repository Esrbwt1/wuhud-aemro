from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from .database import Base # Import Base from our database.py
import datetime

class Note(Base):
    __tablename__ = "notes"

    id = Column(Integer, primary_key=True, index=True)
    content = Column(String, index=True)
    user_id = Column(String, index=True) # Keeping user_id simple for now
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

    # If we had a User model, we could define a relationship here:
    # owner = relationship("User", back_populates="notes") 
    # For now, user_id is just a string identifier.