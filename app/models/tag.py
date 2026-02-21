from typing import List, Optional

from sqlmodel import Field, Relationship, SQLModel

from app.models.links import NoteTagLink


# ── Shared fields ────────────────────────────────────────────────────────────


class TagBase(SQLModel):
    name: str = Field(index=True, min_length=1, max_length=50)
    color: Optional[str] = Field(default=None, max_length=20)  # e.g. "#FF5733"


# ── Table model ──────────────────────────────────────────────────────────────


class Tag(TagBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)

    notes: List["Note"] = Relationship(  # noqa: F821
        back_populates="tags", link_model=NoteTagLink
    )


# ── Request / response schemas ────────────────────────────────────────────────


class TagCreate(TagBase):
    pass


class TagRead(TagBase):
    id: int


class TagReadWithNotes(TagRead):
    # "NoteRead" is resolved via model_rebuild() called in models/__init__.py
    notes: List["NoteRead"] = []  # noqa: F821


class TagUpdate(SQLModel):
    name: Optional[str] = Field(default=None, min_length=1, max_length=50)
    color: Optional[str] = Field(default=None, max_length=20)
