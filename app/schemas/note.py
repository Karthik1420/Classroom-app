from pydantic import BaseModel, Field, EmailStr
from typing import Optional
from datetime import datetime

class NoteBase(BaseModel):
    title: str = Field(..., description="Title of the note")
    description: Optional[str] = Field(None, description="Optional description of the note")
    file_name: Optional[str] = Field(None, description="Original name of the uploaded file")
    classroom_id: int = Field(..., description="ID of the classroom this note belongs to")

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "title": "Week 1 Syllabus",
                    "description": "Reading material for week 1",
                    "file_name": "syllabus.pdf",
                    "classroom_id": 1
                }
            ]
        }
    }

class NoteCreate(NoteBase):
    pass

class NoteOut(NoteBase):
    id: int
    uploaded_by: EmailStr
    created_at: datetime

    class Config:
        from_attributes = True
