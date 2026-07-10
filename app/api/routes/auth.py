from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from app.core.security import create_access_token, verify_password, get_password_hash
from app.core.config import settings
from datetime import timedelta
from app.api import deps

router = APIRouter()

# DUMMY DB for demonstration (Since no User Models should be generated)
DUMMY_USERS = {
    "teacher@example.com": {
        "password_hash": get_password_hash("password123"),
        "role": "teacher"
    },
    "student@example.com": {
        "password_hash": get_password_hash("password123"),
        "role": "student"
    }
}

@router.post(
    "/login/access-token",
    summary="Login to receive access token",
    description="Validates user credentials (email and password) and returns a JWT Bearer token used to authenticate future API requests."
)
def login_access_token(
    form_data: OAuth2PasswordRequestForm = Depends()
):
    """
    OAuth2 compatible token login, get an access token for future requests.
    """
    user = DUMMY_USERS.get(form_data.username)
    
    # 1. Verify email and password
    if not user or not verify_password(form_data.password, user["password_hash"]):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # 2. Token creation
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        subject=form_data.username, role=user["role"], expires_delta=access_token_expires
    )
    
    # 3. Return JWT Access Token
    return {
        "access_token": access_token,
        "token_type": "bearer"
    }

@router.get("/test-token")
def test_token(current_user: str = Depends(deps.get_current_user)):
    """
    Protected API example.
    Test access token validation.
    """
    return {"message": "Token is valid!", "current_user": current_user}
