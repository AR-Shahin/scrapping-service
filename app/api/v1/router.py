from fastapi import APIRouter

from app.api.v1.endpoints import linkedin, youtube

api_router = APIRouter()
api_router.include_router(youtube.router, prefix="/extract", tags=["youtube"])
api_router.include_router(linkedin.router, prefix="/extract", tags=["linkedin"])
