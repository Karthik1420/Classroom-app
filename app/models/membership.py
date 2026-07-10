from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, UniqueConstraint
from sqlalchemy.sql import func
from app.core.database import Base

class ClassroomMembership(Base):
    __tablename__ = "classroom_memberships"

    id = Column(Integer, primary_key=True, index=True)
    
    # Normally this would be a ForeignKey("users.id") pointing to the student.
    # Since we are using logical keys without a User model, it's just an indexed String.
    student_id = Column(String, index=True, nullable=False)
    
    # Foreign Key pointing to the classroom
    classroom_id = Column(Integer, ForeignKey("classrooms.id", ondelete="CASCADE"), nullable=False)
    
    joined_at = Column(DateTime(timezone=True), server_default=func.now())

    # Database-level constraint to prevent a student from joining the same classroom multiple times
    __table_args__ = (
        UniqueConstraint('student_id', 'classroom_id', name='uix_student_classroom'),
    )
