from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from pydantic import ValidationError
from typing import Generator
from app.core.config import settings
from app.core import security
from app.core.database import SessionLocal

def get_db() -> Generator:
    """
    Dependency to get database session.
    Yields a SQLAlchemy session and safely closes it after the request completes.
    """
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()

# OAuth2 context, defines where the client will extract the token from.
# The `tokenUrl` points to the login route we defined in auth.py
reusable_oauth2 = OAuth2PasswordBearer(
    tokenUrl=f"{settings.API_V1_STR}/login/access-token"
)

def get_current_user(token: str = Depends(reusable_oauth2)) -> dict:
    """
    Dependency to get the current logged in user.
    Validates the token, checks expiration, and extracts the user subject and role.
    """
    try:
        # Token validation
        payload = jwt.decode(
            token, settings.SECRET_KEY, algorithms=[settings.JWT_ALGORITHM]
        )
        user_email: str = payload.get("sub")
        user_role: str = payload.get("role")
        if user_email is None or user_role is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Could not validate credentials",
            )
    except (JWTError, ValidationError):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
        )
    
    # Here you would typically fetch the user from the database
    # e.g., user = db.query(User).filter(User.email == user_email).first()
    # if not user: raise HTTPException(status_code=404, detail="User not found")
    
    # Since we are not generating models, we return a dictionary representing the user.
    return {"email": user_email, "role": user_role}

def get_current_teacher(current_user: dict = Depends(get_current_user)) -> dict:
    """
    Dependency to check if the current user has the 'Teacher' role.
    """
    if current_user.get("role") != "teacher":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions. Teacher role required.",
        )
    return current_user

def get_current_student(current_user: dict = Depends(get_current_user)) -> dict:
    """
    Dependency to check if the current user has the 'Student' role.
    """
    if current_user.get("role") != "student":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions. Student role required.",
        )
    return current_user

