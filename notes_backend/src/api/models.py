from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

# PUBLIC_INTERFACE
class Note(BaseModel):
    """Data model for a note."""
    id: int
    title: str
    content: str
    created_at: datetime
    updated_at: datetime

# PUBLIC_INTERFACE
class NoteCreate(BaseModel):
    """Request schema for creating a note."""
    title: str = Field(..., description="Title of the note")
    content: str = Field(..., description="Content of the note")

# PUBLIC_INTERFACE
class NoteUpdate(BaseModel):
    """Request schema for updating a note (partial update allowed)."""
    title: Optional[str] = Field(None, description="Updated title of the note")
    content: Optional[str] = Field(None, description="Updated content of the note")
