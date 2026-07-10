from fastapi import APIRouter, Depends
from app.api import deps

router = APIRouter()

@router.get("/teacher-dashboard")
def teacher_dashboard(current_teacher: dict = Depends(deps.get_current_teacher)):
    """
    Protected API endpoint. Only accessible by users with the 'teacher' role.
    """
    return {
        "message": "Welcome to the Teacher Dashboard!",
        "user_email": current_teacher["email"],
        "role": current_teacher["role"]
    }

@router.get("/student-dashboard")
def student_dashboard(current_student: dict = Depends(deps.get_current_student)):
    """
    Protected API endpoint. Only accessible by users with the 'student' role.
    """
    return {
        "message": "Welcome to the Student Dashboard!",
        "user_email": current_student["email"],
        "role": current_student["role"]
    }

@router.get("/shared-info")
def shared_info(current_user: dict = Depends(deps.get_current_user)):
    """
    Protected API endpoint. Accessible by any authenticated user (either role).
    """
    return {
        "message": "This is shared information accessible by both teachers and students.",
        "user_email": current_user["email"],
        "role": current_user["role"]
    }
