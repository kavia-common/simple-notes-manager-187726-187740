from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .routers import notes

app = FastAPI(
    title="Notes API",
    description="REST API for managing notes. CRUD and search. Built with FastAPI.",
    version="1.0.0",
    openapi_tags=[
        {"name": "notes", "description": "Manage notes (CRUD operations)."},
        {"name": "search", "description": "Search notes by query."},
    ]
)

# Enable CORS for frontend (React at port 3000)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(notes.router)

@app.get("/", tags=["root"], summary="Health check", description="Check backend health status.")
def health_check():
    """Health check endpoint."""
    return {"message": "Healthy"}
