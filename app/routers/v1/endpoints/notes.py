from typing import Any, List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app import cruds, models, schemas
from app.database import connection

router = APIRouter()


@router.get("/", response_model=List[schemas.Note])
def read_notes(
    db: Session = Depends(connection.get_db),
    skip: int = 0,
    limit: int = 25
) -> Any:
    """
    Retrieve notes.
    """
    notes = cruds.note.get_multi(
        db=db, skip=skip, limit=limit
    )
    return notes


@router.post("/", response_model=schemas.Note)
def create_note(
    *,
    db: Session = Depends(connection.get_db),
    note_in: schemas.NoteCreate
) -> Any:
    """
    Create new note.
    """
    note = cruds.note.create(db=db, obj_in=note_in)
    return note


@router.put("/{id}", response_model=schemas.Note)
def update_note(
    *,
    db: Session = Depends(connection.get_db),
    id: int,
    note_in: schemas.NoteUpdate
) -> Any:
    """
    Update an note.
    """
    note = cruds.note.get(db=db, id=id)
    if not note:
        raise HTTPException(status_code=404, detail="Note not found")
    note = cruds.note.update(db=db, db_obj=note, obj_in=note_in)
    return note


@router.get("/{id}", response_model=schemas.Note)
def read_note(
    *,
    db: Session = Depends(connection.get_db),
    id: int
) -> Any:
    """
    Get note by ID.
    """
    note = cruds.note.get(db=db, id=id)
    if not note:
        raise HTTPException(status_code=404, detail="Note not found")
    return note


@router.delete("/{id}", response_model=schemas.Note)
def delete_note(
    *,
    db: Session = Depends(connection.get_db),
    id: int
) -> Any:
    """
    Delete an note.
    """
    note = cruds.note.get(db=db, id=id)
    if not note:
        raise HTTPException(status_code=404, detail="Note not found")
    note = cruds.note.remove(db=db, id=id)
    return note