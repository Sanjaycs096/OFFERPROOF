from datetime import datetime, timezone
import os
import app
from app.schemas.health import HealthResponse


def check_health() -> HealthResponse:
    """
    Check and return the service health status.
    """
    return HealthResponse(
        status="ok",
        service="offerproof-api",
        version=getattr(app, "__version__", "0.2.0"),
        timestamp=datetime.now(timezone.utc),
        environment=os.getenv("ENVIRONMENT", "development"),
    )
