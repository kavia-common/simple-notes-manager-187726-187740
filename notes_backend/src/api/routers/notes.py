from fastapi import APIRouter, Query
from typing import List
from ..models import Note, NoteCreate, NoteUpdate
from ..storage import NotesStore

notes_store = NotesStore()
router = APIRouter()

@router.on_event("startup")
def startup_event():
    """Initialize notes store with sample data."""
    notes_store.load_sample_data()

# PUBLIC_INTERFACE
@router.get("/notes", response_model=List[Note], tags=["notes"], summary="List all notes", description="Returns the full list of notes sorted by created_at descending.")
def list_notes():
    """Get all notes."""
    notes = notes_store.get_all_notes()
    sorted_notes = sorted(notes, key=lambda n: n.created_at, reverse=True)
    return sorted_notes

# PUBLIC_INTERFACE
@router.get("/notes/{note_id}", response_model=Note, tags=["notes"], summary="Get note by ID", description="Return a single note by its integer ID.")
def get_note(note_id: int):
    """Get a note by its ID."""
    return notes_store.get_note(note_id)

# PUBLIC_INTERFACE
@router.post("/notes", response_model=Note, status_code=201, tags=["notes"], summary="Create a new note", description="Create a new note with title and content. Returns created note.")
def create_note(note: NoteCreate):
    """Create a new note."""
    return notes_store.add_note(note)

# PUBLIC_INTERFACE
@router.put("/notes/{note_id}", response_model=Note, tags=["notes"], summary="Update a note", description="Update a note by ID. Only provided fields are updated.")
def update_note(note_id: int, note: NoteUpdate):
    """Update an existing note."""
    return notes_store.update_note(note_id, note)

# PUBLIC_INTERFACE
@router.delete("/notes/{note_id}", status_code=204, tags=["notes"], summary="Delete a note", description="Delete a note by its integer ID. Returns no content.")
def delete_note(note_id: int):
    """Delete a note by ID."""
    notes_store.delete_note(note_id)
    return None

# PUBLIC_INTERFACE
@router.get("/search", response_model=List[Note], tags=["search"], summary="Search notes", description="Search notes by substring in title or content. Query parameter 'query' required.")
def search_notes(query: str = Query(..., min_length=1, description="Search string (at least 1 character)")):
    """Search notes by substring in title or content."""
    return notes_store.search_notes(query)
