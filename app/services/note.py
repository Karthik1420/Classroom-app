from sqlalchemy.orm import Session
from app.models.note import Note
from app.schemas.note import NoteCreate

def create_note(db: Session, note_in: NoteCreate, teacher_id: str) -> Note:
    """
    Creates a new note metadata record in the database.
    """
    db_obj = Note(
        title=note_in.title,
        description=note_in.description,
        file_name=note_in.file_name,
        classroom_id=note_in.classroom_id,
        uploaded_by=teacher_id
    )
    db.add(db_obj)
    db.commit()
    db.refresh(db_obj)
    return db_obj

def get_notes_by_classroom(db: Session, classroom_id: int, skip: int = 0, limit: int = 100):
    """
    Retrieves all notes for a specific classroom.
    """
    return db.query(Note).filter(Note.classroom_id == classroom_id).offset(skip).limit(limit).all()

def update_note_filename(db: Session, note_id: int, file_name: str) -> Note:
    """
    Updates the file_name of a specific note.
    """
    note = db.query(Note).filter(Note.id == note_id).first()
    if note:
        note.file_name = file_name
        db.commit()
        db.refresh(note)
    return note
