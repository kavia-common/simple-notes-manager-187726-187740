from typing import List
from datetime import datetime
from fastapi import HTTPException
import threading

from .models import Note, NoteCreate, NoteUpdate

# PUBLIC_INTERFACE
class NotesStore:
    """In-memory storage backend for notes."""

    def __init__(self):
        self.lock = threading.Lock()
        self.notes: List[Note] = []
        self.counter = 1

    # PUBLIC_INTERFACE
    def get_all_notes(self) -> List[Note]:
        """Return all notes."""
        with self.lock:
            return list(self.notes)

    # PUBLIC_INTERFACE
    def get_note(self, note_id: int) -> Note:
        """Return a note by id."""
        with self.lock:
            note = next((note for note in self.notes if note.id == note_id), None)
            if not note:
                raise HTTPException(status_code=404, detail="Note not found")
            return note

    # PUBLIC_INTERFACE
    def add_note(self, note_create: NoteCreate) -> Note:
        """Add a new note."""
        with self.lock:
            now = datetime.utcnow()
            note = Note(
                id=self.counter,
                title=note_create.title,
                content=note_create.content,
                created_at=now,
                updated_at=now,
            )
            self.notes.append(note)
            self.counter += 1
            return note

    # PUBLIC_INTERFACE
    def update_note(self, note_id: int, note_update: NoteUpdate) -> Note:
        """Update an existing note."""
        with self.lock:
            for i, note in enumerate(self.notes):
                if note.id == note_id:
                    updated_data = note.model_dump()
                    if note_update.title is not None:
                        updated_data["title"] = note_update.title
                    if note_update.content is not None:
                        updated_data["content"] = note_update.content
                    updated_data["updated_at"] = datetime.utcnow()
                    updated_note = Note(**updated_data)
                    self.notes[i] = updated_note
                    return updated_note
            raise HTTPException(status_code=404, detail="Note not found")

    # PUBLIC_INTERFACE
    def delete_note(self, note_id: int) -> None:
        """Delete a note by ID."""
        with self.lock:
            initial_len = len(self.notes)
            self.notes = [note for note in self.notes if note.id != note_id]
            if len(self.notes) == initial_len:
                raise HTTPException(status_code=404, detail="Note not found")

    # PUBLIC_INTERFACE
    def search_notes(self, query: str) -> List[Note]:
        """Search notes by title or content substring (case-insensitive)."""
        with self.lock:
            query_lower = query.lower()
            return [note for note in self.notes if query_lower in note.title.lower() or query_lower in note.content.lower()]

    # PUBLIC_INTERFACE
    def load_sample_data(self):
        """Load some example notes into the store (used at startup)."""
        if len(self.notes) == 0:
            self.add_note(NoteCreate(title="Welcome", content="This is your first note—edit or delete it!"))
            self.add_note(NoteCreate(title="Kavia Notes App", content="Modern notes, fast editing, and instant search."))
