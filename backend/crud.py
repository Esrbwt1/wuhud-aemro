from sqlalchemy.orm import Session
from . import models, schemas # . means current directory
import datetime

def get_note(db: Session, note_id: int):
    """
    Retrieve a single note by its ID.
    """
    return db.query(models.Note).filter(models.Note.id == note_id).first()

def get_notes_by_user(db: Session, user_id: str, skip: int = 0, limit: int = 100):
    """
    Retrieve all notes for a specific user, with pagination.
    """
    return db.query(models.Note).filter(models.Note.user_id == user_id).offset(skip).limit(limit).all()

def create_user_note(db: Session, note: schemas.NoteCreate):
    """
    Create a new note for a user.
    """
    db_note = models.Note(
        content=note.content, 
        user_id=note.user_id,
        created_at=datetime.datetime.utcnow() # Explicitly set here, though model has default
    )
    db.add(db_note)
    db.commit()
    db.refresh(db_note) # Refresh to get the ID and other generated values like created_at
    return db_note

# We can add update_note and delete_note functions here later if needed.
# def update_note(...):
#     pass

# def delete_note(...):
#     pass