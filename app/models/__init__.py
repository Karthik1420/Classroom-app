# Import all models here to ensure Alembic can discover them
from app.core.database import Base
from app.models.classroom import Classroom
from app.models.membership import ClassroomMembership
from app.models.note import Note
