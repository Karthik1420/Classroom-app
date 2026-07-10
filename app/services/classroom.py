import uuid
from sqlalchemy.orm import Session
from app.models.classroom import Classroom
from app.schemas.classroom import ClassroomCreate

def get_classroom_by_code(db: Session, code: str):
    """
    Retrieves a classroom by its unique code.
    """
    return db.query(Classroom).filter(Classroom.classroom_code == code).first()

def generate_unique_classroom_code(db: Session) -> str:
    """
    Generates a short, unique 8-character code for joining the classroom.
    Validates uniqueness against the database before returning.
    """
    while True:
        code = str(uuid.uuid4())[:8].upper()
        # Ensure the generated code does not already exist in the DB
        if not get_classroom_by_code(db, code):
            return code

def create_classroom(db: Session, classroom_in: ClassroomCreate, teacher_id: str) -> Classroom:
    """
    Creates a new classroom in the database.
    """
    db_obj = Classroom(
        classroom_name=classroom_in.classroom_name,
        description=classroom_in.description,
        classroom_code=generate_unique_classroom_code(db),
        teacher_id=teacher_id
    )
    db.add(db_obj)
    db.commit()
    db.refresh(db_obj)
    return db_obj

def get_classrooms_by_teacher(db: Session, teacher_id: str, skip: int = 0, limit: int = 100):
    """
    Retrieves all classrooms that belong to a specific teacher.
    """
    return db.query(Classroom).filter(Classroom.teacher_id == teacher_id).offset(skip).limit(limit).all()
