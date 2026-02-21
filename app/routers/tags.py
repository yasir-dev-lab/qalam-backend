from typing import List

from fastapi import APIRouter, Depends
from sqlmodel import Session

from app.database import get_session
from app.models import TagCreate, TagRead, TagReadWithNotes, TagUpdate
from app.services import tag_service

router = APIRouter(prefix="/tags", tags=["Tags"])


@router.get("/", response_model=List[TagRead])
def list_tags(session: Session = Depends(get_session)):
    """Return all tags ordered by name."""
    return tag_service.list_tags(session)


@router.post("/", response_model=TagRead, status_code=201)
def create_tag(data: TagCreate, session: Session = Depends(get_session)):
    """Create a new tag."""
    return tag_service.create_tag(session, data)


@router.get("/{tag_id}", response_model=TagReadWithNotes)
def get_tag(tag_id: int, session: Session = Depends(get_session)):
    """Get a tag by ID, including the list of notes it is applied to."""
    return tag_service.get_tag(session, tag_id)


@router.patch("/{tag_id}", response_model=TagRead)
def update_tag(
    tag_id: int,
    data: TagUpdate,
    session: Session = Depends(get_session),
):
    """Partially update a tag's name or color."""
    return tag_service.update_tag(session, tag_id, data)


@router.delete("/{tag_id}", status_code=204)
def delete_tag(tag_id: int, session: Session = Depends(get_session)):
    """Delete a tag and remove it from all notes."""
    tag_service.delete_tag(session, tag_id)
