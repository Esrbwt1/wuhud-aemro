from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List # For response models that return a list

# Import components from our other backend files
from . import crud, models, schemas # Note the "." for relative imports
from .database import SessionLocal, engine, get_db

# Create all database tables (if they don't exist already)
# This line should be called when the application starts.
# For a more robust setup with migrations (e.g., Alembic), this might be handled differently.
models.Base.metadata.create_all(bind=engine)

# Initialize FastAPI app
app = FastAPI(
    title="WuhudA'emro API",
    version="0.0.2", # Incremented version
    description="The foundational API for the Personalized AI Symbiosis Platform, now with persistent storage."
)

# --- API Endpoints ---

@app.get("/")
async def read_root():
    """
    Root endpoint for the API.
    Provides a welcome message and basic API information.
    """
    return {
        "message": "Welcome to WuhudA'emro API!",
        "version": app.version,
        "documentation_url": "/docs"
    }

@app.post("/notes/", response_model=schemas.Note, status_code=201)
async def create_note_endpoint(note: schemas.NoteCreate, db: Session = Depends(get_db)):
    """
    Endpoint to create a new note.
    The note is now stored in the SQLite database.
    - `note: schemas.NoteCreate`: The request body, validated by Pydantic.
    - `db: Session = Depends(get_db)`: Injects a database session.
    - `response_model=schemas.Note`: Specifies the shape of the successful response.
    """
    return crud.create_user_note(db=db, note=note)

@app.get("/notes/user/{user_id}", response_model=List[schemas.Note])
async def get_notes_for_user_endpoint(user_id: str, skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """
    Endpoint to retrieve all notes for a specific user.
    - `user_id`: Path parameter.
    - `skip`, `limit`: Query parameters for pagination.
    - `response_model=List[schemas.Note]`: Indicates the response is a list of Note objects.
    """
    notes = crud.get_notes_by_user(db=db, user_id=user_id, skip=skip, limit=limit)
    if not notes:
        # You could return an empty list and 200 OK, or a 404 if preferred.
        # For now, returning empty list is fine.
        return []
    return notes

@app.get("/notes/{note_id}", response_model=schemas.Note)
async def get_single_note_endpoint(note_id: int, db: Session = Depends(get_db)):
    """
    Endpoint to retrieve a single note by its ID.
    """
    db_note = crud.get_note(db=db, note_id=note_id)
    if db_note is None:
        raise HTTPException(status_code=404, detail="Note not found")
    return db_note

# Note: The if __name__ == "__main__": block for uvicorn.run is removed.
# It's better practice to run uvicorn directly from the command line as we've been doing:
# `uvicorn main:app --reload`
# This ensures that `models.Base.metadata.create_all(bind=engine)` runs correctly in the global scope
# when the Uvicorn server imports the `app` object.