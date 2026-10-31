from fastapi import APIRouter
from app.routes.health import router as health_router
from app.routes.ingestion import router as ingestion_router
from app.routes.verification import router as verification_router

api_router = APIRouter()
api_router.include_router(health_router)
api_router.include_router(ingestion_router)
api_router.include_router(verification_router)

__all__ = ["api_router"]
