from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.exc import IntegrityError
from app.core.config import settings
from app.api.routes import api_router
from app.core.database import engine, Base
import app.models.classroom
import app.models.membership
import app.models.note

def get_application() -> FastAPI:
    """
    Initialize FastAPI application with specific configurations
    """
    # Create the app instance with metadata for Swagger documentation
    app = FastAPI(
        title=settings.PROJECT_NAME,
        openapi_url=f"{settings.API_V1_STR}/openapi.json",
        description="Classroom Management System API",
        version="1.0.0"
    )

    # Configure CORS (Cross-Origin Resource Sharing)
    # Allows frontend applications to communicate with this backend
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"], # In production, replace with specific origins
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # Create all database tables (Normally handled by Alembic migrations in production)
    Base.metadata.create_all(bind=engine)

    # Include all API routes
    app.include_router(api_router, prefix=settings.API_V1_STR)
    
    # --- Centralized Exception Handling ---
    @app.exception_handler(IntegrityError)
    async def sqlalchemy_integrity_error_handler(request: Request, exc: IntegrityError):
        """
        Catches database integrity errors globally (e.g., duplicate unique constraint).
        Returns a clean 409 Conflict instead of a 500 Internal Server Error.
        """
        return JSONResponse(
            status_code=409,
            content={"detail": "Database conflict: A resource with these unique values already exists."}
        )
        
    @app.exception_handler(Exception)
    async def global_exception_handler(request: Request, exc: Exception):
        """
        Catches any unhandled exceptions to prevent leaking stack traces to the client.
        """
        return JSONResponse(
            status_code=500,
            content={"detail": "An unexpected error occurred. Please contact support."}
        )

    return app

app = get_application()

if __name__ == "__main__":
    import uvicorn
    # Run the application using Uvicorn server
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
