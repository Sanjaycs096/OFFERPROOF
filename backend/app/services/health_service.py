from datetime import datetime, timezone
import os
from app.schemas.health import HealthResponse


def check_health() -> HealthResponse:
    """
    Check and return the service health status.
    """
    return HealthResponse(
        status="ok",
        service="offerproof-api",
        version="0.1.0",
        timestamp=datetime.now(timezone.utc),
        environment=os.getenv("ENVIRONMENT", "development"),
    )
