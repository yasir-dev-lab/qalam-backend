from datetime import datetime, timezone
from typing import List, Optional

from sqlmodel import Field, Relationship, SQLModel

from app.models.links import NoteTagLink


# ── Shared fields ────────────────────────────────────────────────────────────


class NoteBase(SQLModel):
    title: str = Field(min_length=1, max_length=255)
    body: Optional[str] = Field(default=None)  # Markdown content


# ── Table model ──────────────────────────────────────────────────────────────


def _utcnow() -> datetime:
    return datetime.now(timezone.utc)


class Note(NoteBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    created_at: datetime = Field(default_factory=_utcnow)
    updated_at: datetime = Field(default_factory=_utcnow)

    tags: List["Tag"] = Relationship(  # noqa: F821
        back_populates="notes", link_model=NoteTagLink
    )


# ── Request / response schemas ────────────────────────────────────────────────


class NoteCreate(NoteBase):
    pass


class NoteRead(NoteBase):
    id: int
    created_at: datetime
    updated_at: datetime


class NoteReadWithTags(NoteRead):
    # "TagRead" is resolved via model_rebuild() called in models/__init__.py
    tags: List["TagRead"] = []  # noqa: F821


class NoteUpdate(SQLModel):
    title: Optional[str] = Field(default=None, min_length=1, max_length=255)
    body: Optional[str] = None
