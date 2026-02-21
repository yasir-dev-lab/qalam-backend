from typing import List, Optional, Sequence

from fastapi import HTTPException, status
from sqlmodel import Session, select

from app.models import Tag, TagCreate, TagUpdate


def create_tag(session: Session, data: TagCreate) -> Tag:
    # Prevent duplicate tag names (case-insensitive)
    existing = session.exec(
        select(Tag).where(Tag.name == data.name)
    ).first()
    if existing:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"Tag with name '{data.name}' already exists.",
        )
    tag = Tag.model_validate(data)
    session.add(tag)
    session.commit()
    session.refresh(tag)
    return tag


def get_tag(session: Session, tag_id: int) -> Tag:
    tag = session.get(Tag, tag_id)
    if not tag:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Tag {tag_id} not found.",
        )
    return tag


def list_tags(session: Session) -> Sequence[Tag]:
    return session.exec(select(Tag).order_by(Tag.name)).all()


def update_tag(session: Session, tag_id: int, data: TagUpdate) -> Tag:
    tag = get_tag(session, tag_id)
    update_dict = data.model_dump(exclude_unset=True)
    if "name" in update_dict and update_dict["name"] != tag.name:
        conflict = session.exec(
            select(Tag).where(Tag.name == update_dict["name"])
        ).first()
        if conflict:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=f"Tag with name '{update_dict['name']}' already exists.",
            )
    tag.sqlmodel_update(update_dict)
    session.add(tag)
    session.commit()
    session.refresh(tag)
    return tag


def delete_tag(session: Session, tag_id: int) -> None:
    tag = get_tag(session, tag_id)
    session.delete(tag)
    session.commit()
