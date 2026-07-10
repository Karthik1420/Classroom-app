from pydantic import BaseModel, Field, EmailStr
from typing import Optional
from datetime import datetime

class ClassroomBase(BaseModel):
    classroom_name: str = Field(..., description="Name of the classroom")
    description: Optional[str] = Field(None, description="Optional description of the classroom")

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "classroom_name": "Mathematics 101",
                    "description": "Introduction to Algebra"
                }
            ]
        }
    }

class ClassroomCreate(ClassroomBase):
    pass

class ClassroomOut(ClassroomBase):
    id: int
    classroom_code: str
    teacher_id: EmailStr
    created_at: datetime

    class Config:
        from_attributes = True
