from sqlmodel import Field, SQLModel


class NoteTagLink(SQLModel, table=True):
    """Join table for the Note <-> Tag many-to-many relationship."""

    note_id: int | None = Field(default=None, foreign_key="note.id", primary_key=True)
    tag_id: int | None = Field(default=None, foreign_key="tag.id", primary_key=True)
