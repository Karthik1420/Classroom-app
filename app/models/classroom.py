from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.sql import func
from app.core.database import Base

class Classroom(Base):
    __tablename__ = "classrooms"

    id = Column(Integer, primary_key=True, index=True)
    classroom_name = Column(String, index=True, nullable=False)
    description = Column(String, nullable=True)
    classroom_code = Column(String, unique=True, index=True, nullable=False)
    
    # Note: As per requirements to not generate a User model, this acts as a logical Foreign Key.
    # In a full implementation with a User model, this would be: Column(Integer, ForeignKey("users.id"))
    teacher_id = Column(String, index=True, nullable=False)
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())
