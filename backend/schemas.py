from pydantic import BaseModel
from typing import Optional
import datetime

# Base schema for common attributes
class NoteBase(BaseModel):
    content: str
    user_id: str

# Schema for creating a note (inherits from NoteBase)
# This is what the API will expect in the request body for creating a note.
class NoteCreate(NoteBase):
    pass

# Schema for reading/returning a note from the API (inherits from NoteBase)
# This includes attributes that are in the database but not necessarily in the create request.
class Note(NoteBase):
    id: int
    created_at: datetime.datetime

    class Config:
        orm_mode = True # Pydantic's orm_mode will tell Pydantic to read the data even if it is not a dict, but an ORM model.