import os
import uuid
import shutil
from typing import List
from fastapi import APIRouter, Depends, HTTPException, status, File, UploadFile, Path, Query
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session
from app.api.deps import get_db
from app.schemas.note import NoteCreate, NoteOut
from app.models.classroom import Classroom
from app.models.note import Note
from app.models.membership import ClassroomMembership
from app.services import note as crud_note
from app.api import deps

router = APIRouter()

UPLOAD_DIR = "uploaded_notes"
os.makedirs(UPLOAD_DIR, exist_ok=True)

@router.post(
    "/", 
    response_model=NoteOut, 
    status_code=status.HTTP_201_CREATED,
    summary="Create note metadata",
    description="Creates a new note record inside a classroom. This endpoint only accepts metadata; the actual PDF file must be uploaded using the subsequent upload endpoint."
)
def create_note(
    *,
    db: Session = Depends(get_db),
    note_in: NoteCreate,
    current_teacher: dict = Depends(deps.get_current_teacher)
):
    """
    Create a new note in a classroom (Metadata only).
    Only accessible by the teacher who created the classroom.
    """
    teacher_id = current_teacher["email"]
    
    # Validate classroom exists
    classroom = db.query(Classroom).filter(Classroom.id == note_in.classroom_id).first()
    if not classroom:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Classroom not found")
        
    # Enforce Business Rule: Teachers can only create notes in classrooms they own
    if classroom.teacher_id != teacher_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="You can only create notes in classrooms you own.")
        
    return crud_note.create_note(db=db, note_in=note_in, teacher_id=teacher_id)

def _get_note_and_classroom_or_404(db: Session, note_id: int):
    """
    Helper function to reduce duplicate code.
    Fetches the Note and its parent Classroom, raising a 404 if either is missing.
    """
    note = db.query(Note).filter(Note.id == note_id).first()
    if not note:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Note not found")
        
    classroom = db.query(Classroom).filter(Classroom.id == note.classroom_id).first()
    if not classroom:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Classroom not found")
        
    return note, classroom

@router.get(
    "/classroom/{classroom_id}", 
    response_model=List[NoteOut],
    summary="List classroom notes",
    description="Retrieves a list of all notes available in a specific classroom. Accessible by the owning teacher or enrolled students."
)
def list_notes(
    classroom_id: int = Path(..., description="The ID of the classroom to query"),
    db: Session = Depends(get_db),
    skip: int = Query(0, description="Number of records to skip for pagination"),
    limit: int = Query(100, description="Maximum number of records to return"),
    current_user: dict = Depends(deps.get_current_user)
):
    """
    List notes for a specific classroom.
    Checks authorization to ensure the user is either the teacher who owns the classroom
    or a student who has joined the classroom.
    """
    user_email = current_user["email"]
    user_role = current_user["role"]
    
    classroom = db.query(Classroom).filter(Classroom.id == classroom_id).first()
    if not classroom:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Classroom not found")

    # Authorization Check
    if user_role == "teacher":
        if classroom.teacher_id != user_email:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="You do not own this classroom.")
    elif user_role == "student":
        is_member = db.query(ClassroomMembership).filter(
            ClassroomMembership.classroom_id == classroom_id,
            ClassroomMembership.student_id == user_email
        ).first()
        if not is_member:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="You must join the classroom to view notes.")

    return crud_note.get_notes_by_classroom(db=db, classroom_id=classroom_id, skip=skip, limit=limit)

@router.post(
    "/{note_id}/upload", 
    response_model=NoteOut,
    summary="Upload note PDF",
    description="Uploads a PDF file and attaches it to an existing note record. Replaces the file name in the database with a unique safe filename."
)
def upload_note_file(
    note_id: int = Path(..., description="The ID of the note to attach the file to"),
    file: UploadFile = File(..., description="The PDF file to upload"),
    db: Session = Depends(get_db),
    current_teacher: dict = Depends(deps.get_current_teacher)
):
    """
    Upload a PDF file for an existing note.
    Only accessible by the teacher who created the classroom.
    """
    teacher_id = current_teacher["email"]
    
    # 1 & 2. Fetch the note and classroom
    note, classroom = _get_note_and_classroom_or_404(db, note_id)
    
    if classroom.teacher_id != teacher_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, 
            detail="You can only upload files to classrooms you own."
        )
        
    # 3. Validate file type (must be PDF)
    if file.content_type != "application/pdf" or not file.filename.lower().endswith(".pdf"):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, 
            detail="Only PDF files are allowed."
        )
        
    # 4. Generate unique filename and save
    unique_filename = f"{uuid.uuid4()}_{file.filename}"
    file_path = os.path.join(UPLOAD_DIR, unique_filename)
    
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
        
    # 5. Update the note record
    updated_note = crud_note.update_note_filename(db=db, note_id=note_id, file_name=unique_filename)
    
    return updated_note

def serve_note_file(note_id: int, db: Session, current_user: dict, disposition: str):
    """
    Helper function to enforce authorization and return the file response.
    """
    user_email = current_user["email"]
    user_role = current_user["role"]
    
    note, classroom = _get_note_and_classroom_or_404(db, note_id)

    # Authorization Check
    if user_role == "teacher":
        if classroom.teacher_id != user_email:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="You do not own this classroom.")
    elif user_role == "student":
        is_member = db.query(ClassroomMembership).filter(
            ClassroomMembership.classroom_id == classroom.id,
            ClassroomMembership.student_id == user_email
        ).first()
        if not is_member:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="You must join the classroom to access its files.")
            
    file_path = os.path.join(UPLOAD_DIR, note.file_name)
    if not os.path.exists(file_path):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="File not found on server")
        
    download_name = f"{note.title}.pdf"

    return FileResponse(
        path=file_path,
        media_type="application/pdf",
        filename=download_name,
        content_disposition_type=disposition
    )

@router.get(
    "/{note_id}/file",
    summary="View note PDF",
    description="Returns the PDF file inline, allowing it to be viewed directly inside a web browser."
)
def view_note_file(
    note_id: int = Path(..., description="The ID of the note to view"),
    db: Session = Depends(get_db),
    current_user: dict = Depends(deps.get_current_user)
):
    """
    Open the PDF file in the browser (inline viewing).
    """
    return serve_note_file(note_id, db, current_user, disposition="inline")

@router.get(
    "/{note_id}/download",
    summary="Download note PDF",
    description="Returns the PDF file as an attachment, forcing the browser to download the file to the user's device."
)
def download_note_file(
    note_id: int = Path(..., description="The ID of the note to download"),
    db: Session = Depends(get_db),
    current_user: dict = Depends(deps.get_current_user)
):
    """
    Download the PDF file as an attachment.
    """
    return serve_note_file(note_id, db, current_user, disposition="attachment")
