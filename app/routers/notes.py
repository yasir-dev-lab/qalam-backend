from typing import List, Optional

from fastapi import APIRouter, Depends, Query
from sqlmodel import Session

from app.database import get_session
from app.models import NoteCreate, NoteRead, NoteReadWithTags, NoteUpdate
from app.services import note_service

router = APIRouter(prefix="/notes", tags=["Notes"])


@router.get("/", response_model=List[NoteReadWithTags])
def list_notes(
    q: Optional[str] = Query(default=None, description="Keyword search in title or body"),
    tag_id: Optional[int] = Query(default=None, description="Filter by tag ID"),
    offset: int = Query(default=0, ge=0, description="Pagination offset"),
    limit: int = Query(default=50, ge=1, le=200, description="Max results to return"),
    session: Session = Depends(get_session),
):
    """List notes, newest first. Optionally filter by keyword and/or tag."""
    return note_service.list_notes(session, q=q, tag_id=tag_id, offset=offset, limit=limit)


@router.post("/", response_model=NoteReadWithTags, status_code=201)
def create_note(data: NoteCreate, session: Session = Depends(get_session)):
    """Create a new note."""
    return note_service.create_note(session, data)


@router.get("/{note_id}", response_model=NoteReadWithTags)
def get_note(note_id: int, session: Session = Depends(get_session)):
    """Get a note by ID, including all its tags."""
    return note_service.get_note(session, note_id)


@router.patch("/{note_id}", response_model=NoteReadWithTags)
def update_note(
    note_id: int,
    data: NoteUpdate,
    session: Session = Depends(get_session),
):
    """Partially update a note's title or body. Automatically bumps updated_at."""
    return note_service.update_note(session, note_id, data)


@router.delete("/{note_id}", status_code=204)
def delete_note(note_id: int, session: Session = Depends(get_session)):
    """Delete a note and all its tag associations."""
    note_service.delete_note(session, note_id)


@router.post("/{note_id}/tags/{tag_id}", response_model=NoteReadWithTags)
def attach_tag(
    note_id: int,
    tag_id: int,
    session: Session = Depends(get_session),
):
    """Attach an existing tag to a note."""
    return note_service.attach_tag(session, note_id, tag_id)


@router.delete("/{note_id}/tags/{tag_id}", response_model=NoteReadWithTags)
def detach_tag(
    note_id: int,
    tag_id: int,
    session: Session = Depends(get_session),
):
    """Remove a tag from a note (does not delete the tag itself)."""
    return note_service.detach_tag(session, note_id, tag_id)
