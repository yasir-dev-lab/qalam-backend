# Import order matters: links must come before tag and note (foreign keys).
from app.models.links import NoteTagLink  # noqa: F401
from app.models.tag import Tag, TagBase, TagCreate, TagRead, TagReadWithNotes, TagUpdate  # noqa: F401
from app.models.note import Note, NoteBase, NoteCreate, NoteRead, NoteReadWithTags, NoteUpdate  # noqa: F401

# Resolve cross-model forward references now that both modules are loaded.
NoteReadWithTags.model_rebuild()
TagReadWithNotes.model_rebuild()

__all__ = [
    "NoteTagLink",
    "Tag", "TagBase", "TagCreate", "TagRead", "TagReadWithNotes", "TagUpdate",
    "Note", "NoteBase", "NoteCreate", "NoteRead", "NoteReadWithTags", "NoteUpdate",
]
