from typing import List
from fastapi import APIRouter, Depends, HTTPException, status, Query, Path
from sqlalchemy.orm import Session
from app.api.deps import get_db
from app.models.classroom import Classroom
from app.schemas.classroom import ClassroomCreate, ClassroomOut
from app.schemas.membership import JoinClassroomRequest, ClassroomMembershipOut, EnrolledStudentOut
from app.services import classroom as crud_classroom
from app.services import membership as crud_membership
from app.api import deps

router = APIRouter()

@router.post(
    "/", 
    response_model=ClassroomOut, 
    status_code=status.HTTP_201_CREATED,
    summary="Create a new classroom",
    description="Creates a new classroom. Automatically assigns the currently authenticated teacher as the owner."
)
def create_classroom(
    *,
    db: Session = Depends(get_db),
    classroom_in: ClassroomCreate,
    current_teacher: dict = Depends(deps.get_current_teacher)
):
    """
    Create a new classroom. 
    Only accessible by users with the 'Teacher' role.
    """
    # The teacher_id is obtained from the JWT token of the currently authenticated teacher
    teacher_id = current_teacher["email"]
    return crud_classroom.create_classroom(db=db, classroom_in=classroom_in, teacher_id=teacher_id)

@router.get(
    "/", 
    response_model=List[ClassroomOut],
    summary="List teacher's classrooms",
    description="Retrieves a paginated list of classrooms created by the currently authenticated teacher."
)
def list_classrooms(
    db: Session = Depends(get_db),
    skip: int = Query(0, description="Number of records to skip for pagination"),
    limit: int = Query(100, description="Maximum number of records to return"),
    current_teacher: dict = Depends(deps.get_current_teacher)
):
    """
    List classrooms created by the current teacher.
    Only accessible by users with the 'Teacher' role.
    """
    teacher_id = current_teacher["email"]
    return crud_classroom.get_classrooms_by_teacher(db=db, teacher_id=teacher_id, skip=skip, limit=limit)

@router.get(
    "/joined", 
    response_model=List[ClassroomOut],
    summary="List joined classrooms",
    description="Retrieves a list of classrooms that the currently authenticated student has joined."
)
def list_joined_classrooms(
    db: Session = Depends(get_db),
    current_student: dict = Depends(deps.get_current_student)
):
    """
    List classrooms that the current student has joined.
    Only accessible by users with the 'Student' role.
    """
    student_id = current_student["email"]
    return crud_membership.get_classrooms_for_student(db=db, student_id=student_id)

@router.get(
    "/{classroom_id}/students", 
    response_model=List[EnrolledStudentOut],
    summary="List enrolled students",
    description="Retrieves a list of students enrolled in a specific classroom. The authenticated teacher must own the classroom."
)
def list_enrolled_students(
    classroom_id: int = Path(..., description="The ID of the classroom to query"),
    db: Session = Depends(get_db),
    current_teacher: dict = Depends(deps.get_current_teacher)
):
    """
    List students enrolled in a specific classroom.
    Only accessible by the teacher who created the classroom.
    """
    teacher_id = current_teacher["email"]
    
    # 1. Validate classroom exists
    classroom = db.query(Classroom).filter(Classroom.id == classroom_id).first()
    if not classroom:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail="Classroom not found"
        )
        
    # 2. Authorize: Ensure the current teacher actually owns this classroom
    if classroom.teacher_id != teacher_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, 
            detail="You do not have permission to view students for this classroom."
        )
        
    return crud_membership.get_students_in_classroom(db=db, classroom_id=classroom_id)

@router.post(
    "/join", 
    response_model=ClassroomMembershipOut, 
    status_code=status.HTTP_201_CREATED,
    summary="Join a classroom",
    description="Allows a student to join a classroom using the unique 8-character classroom code."
)
def join_classroom(
    *,
    db: Session = Depends(get_db),
    join_request: JoinClassroomRequest,
    current_student: dict = Depends(deps.get_current_student)
):
    """
    Join a classroom using a unique classroom code.
    Only accessible by users with the 'Student' role.
    Teachers attempting to use this will receive a 403 Forbidden.
    """
    student_id = current_student["email"]
    return crud_membership.join_classroom(
        db=db, 
        classroom_code=join_request.classroom_code, 
        student_id=student_id
    )
