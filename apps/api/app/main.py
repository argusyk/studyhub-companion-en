from fastapi import APIRouter, FastAPI

from app.routers import health, labs, submissions

app = FastAPI(title="StudyHub API", version="0.1.0")

# The single API prefix is set here, not in individual routers.
api = APIRouter(prefix="/api/v1")
api.include_router(health.router)
api.include_router(labs.router)
api.include_router(submissions.router)
app.include_router(api)
