from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.sql import func
from app.core.database import Base

class Note(Base):
    __tablename__ = "notes"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True, nullable=False)
    description = Column(String, nullable=True)
    file_name = Column(String, nullable=False)
    
    # Foreign Key pointing to the classroom
    classroom_id = Column(Integer, ForeignKey("classrooms.id", ondelete="CASCADE"), nullable=False)
    
    # Logical Foreign Key pointing to the User who uploaded the note
    uploaded_by = Column(String, index=True, nullable=False)
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())
