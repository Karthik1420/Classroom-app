from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from app.models.membership import ClassroomMembership
from app.models.classroom import Classroom

def join_classroom(db: Session, classroom_code: str, student_id: str) -> ClassroomMembership:
    """
    Business logic for a student joining a classroom.
    Validates code and prevents duplicate joins.
    """
    # 1. Validate the classroom code exists
    classroom = db.query(Classroom).filter(Classroom.classroom_code == classroom_code).first()
    if not classroom:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail="Invalid classroom code."
        )
    
    # 2. Prevent duplicate joins (verify they aren't already a member)
    existing_membership = db.query(ClassroomMembership).filter(
        ClassroomMembership.student_id == student_id,
        ClassroomMembership.classroom_id == classroom.id
    ).first()
    
    if existing_membership:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT, 
            detail="You have already joined this classroom."
        )
        
    # 3. Create and save the new membership relationship
    new_membership = ClassroomMembership(
        student_id=student_id,
        classroom_id=classroom.id
    )
    db.add(new_membership)
    db.commit()
    db.refresh(new_membership)
    
    return new_membership

def get_students_in_classroom(db: Session, classroom_id: int):
    """
    Retrieves all membership records (students) for a specific classroom.
    """
    return db.query(ClassroomMembership).filter(ClassroomMembership.classroom_id == classroom_id).all()

def get_classrooms_for_student(db: Session, student_id: str):
    """
    Retrieves all classrooms that a specific student has joined.
    """
    return db.query(Classroom).join(ClassroomMembership).filter(ClassroomMembership.student_id == student_id).all()

