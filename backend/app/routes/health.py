from fastapi import APIRouter
from app.schemas.health import HealthResponse
from app.services.health_service import check_health

router = APIRouter(tags=["Health"])


@router.get("/health", response_model=HealthResponse, summary="Service Health Check")
def get_health() -> HealthResponse:
    """
    Returns backend service health, version, and server timestamp.
    """
    return check_health()
