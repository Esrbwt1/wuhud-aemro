from fastapi import FastAPI
from pydantic import BaseModel
import uvicorn

# Initialize FastAPI app
app = FastAPI(
    title="WuhudA'emro API",
    version="0.0.1",
    description="The foundational API for the Personalized AI Symbiosis Platform."
)

# Pydantic model for request body (for later use)
class Note(BaseModel):
    content: str
    user_id: str # For now, just a string. Will be more complex later.

# In-memory storage for notes (temporary, will be replaced by a database)
# Using a dictionary where key is user_id and value is a list of notes for that user
mock_db_notes = {}

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

@app.post("/notes/", status_code=201)
async def create_note(note: Note):
    """
    Endpoint to create a new note.
    For now, it stores the note in an in-memory dictionary.
    """
    if note.user_id not in mock_db_notes:
        mock_db_notes[note.user_id] = []
    
    mock_db_notes[note.user_id].append(note.content)
    
    return {
        "message": "Note created successfully",
        "user_id": note.user_id,
        "note_content": note.content,
        "total_notes_for_user": len(mock_db_notes[note.user_id])
    }

@app.get("/notes/{user_id}")
async def get_notes_for_user(user_id: str):
    """
    Endpoint to retrieve all notes for a specific user.
    """
    if user_id not in mock_db_notes:
        return {"message": "No notes found for this user.", "notes": []}
    
    return {"user_id": user_id, "notes": mock_db_notes[user_id]}

if __name__ == "__main__":
    # This block allows running the app directly with `python main.py`
    # However, for development, `uvicorn main:app --reload` is preferred.
    print("Starting Uvicorn server on http://127.0.0.1:8000")
    uvicorn.run(app, host="127.0.0.1", port=8000)