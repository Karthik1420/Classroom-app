from pydantic import BaseModel, Field, EmailStr
from datetime import datetime

class JoinClassroomRequest(BaseModel):
    classroom_code: str = Field(..., min_length=8, max_length=8, description="The 8-character unique classroom code")

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "classroom_code": "A1B2C3D4"
                }
            ]
        }
    }

class ClassroomMembershipOut(BaseModel):
    id: int
    student_id: EmailStr
    classroom_id: int
    joined_at: datetime

    class Config:
        from_attributes = True

class EnrolledStudentOut(BaseModel):
    student_id: str
    joined_at: datetime

    class Config:
        from_attributes = True
