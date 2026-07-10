from fastapi import APIRouter

api_router = APIRouter()

# Example of including a route
from app.api.routes import auth, rbac_demo, classrooms, notes
api_router.include_router(auth.router, tags=["login"])
api_router.include_router(rbac_demo.router, prefix="/rbac", tags=["rbac"])
api_router.include_router(classrooms.router, prefix="/classrooms", tags=["classrooms"])
api_router.include_router(notes.router, prefix="/notes", tags=["notes"])

@api_router.get("/health")
def health_check():
    return {"status": "healthy"}
