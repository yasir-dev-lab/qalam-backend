from datetime import datetime, timezone
from typing import Optional, Sequence

from fastapi import HTTPException, status
from sqlmodel import Session, col, select

from app.models import Note, NoteCreate, NoteTagLink, NoteUpdate, Tag


def create_note(session: Session, data: NoteCreate) -> Note:
    note = Note.model_validate(data)
    session.add(note)
    session.commit()
    session.refresh(note)
    return note


def get_note(session: Session, note_id: int) -> Note:
    note = session.get(Note, note_id)
    if not note:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Note {note_id} not found.",
        )
    return note


def list_notes(
    session: Session,
    q: Optional[str] = None,
    tag_id: Optional[int] = None,
    offset: int = 0,
    limit: int = 50,
) -> Sequence[Note]:
    """
    List notes with optional filters:
      - q        : case-insensitive keyword search in title OR body
      - tag_id   : only return notes that have this tag attached
      - offset / limit : pagination
    """
    statement = select(Note)

    if tag_id is not None:
        statement = (
            statement.join(NoteTagLink, NoteTagLink.note_id == col(Note.id))
            .where(NoteTagLink.tag_id == tag_id)
        )

    if q:
        keyword = f"%{q}%"
        statement = statement.where(
            col(Note.title).ilike(keyword) | col(Note.body).ilike(keyword)
        )

    statement = (
        statement.order_by(col(Note.updated_at).desc())
        .offset(offset)
        .limit(limit)
    )
    return session.exec(statement).all()


def update_note(session: Session, note_id: int, data: NoteUpdate) -> Note:
    note = get_note(session, note_id)
    update_dict = data.model_dump(exclude_unset=True)
    update_dict["updated_at"] = datetime.now(timezone.utc)
    note.sqlmodel_update(update_dict)
    session.add(note)
    session.commit()
    session.refresh(note)
    return note


def delete_note(session: Session, note_id: int) -> None:
    note = get_note(session, note_id)
    session.delete(note)
    session.commit()


def attach_tag(session: Session, note_id: int, tag_id: int) -> Note:
    note = get_note(session, note_id)
    tag = session.get(Tag, tag_id)
    if not tag:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Tag {tag_id} not found.",
        )

    # Check if link already exists
    existing_link = session.exec(
        select(NoteTagLink)
        .where(NoteTagLink.note_id == note_id)
        .where(NoteTagLink.tag_id == tag_id)
    ).first()
    if existing_link:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"Tag {tag_id} is already attached to note {note_id}.",
        )

    link = NoteTagLink(note_id=note_id, tag_id=tag_id)
    session.add(link)
    session.commit()
    session.refresh(note)
    return note


def detach_tag(session: Session, note_id: int, tag_id: int) -> Note:
    note = get_note(session, note_id)
    link = session.exec(
        select(NoteTagLink)
        .where(NoteTagLink.note_id == note_id)
        .where(NoteTagLink.tag_id == tag_id)
    ).first()
    if not link:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Tag {tag_id} is not attached to note {note_id}.",
        )
    session.delete(link)
    session.commit()
    session.refresh(note)
    return note
