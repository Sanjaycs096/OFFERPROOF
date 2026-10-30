from datetime import datetime
from pydantic import BaseModel, Field


class HealthResponse(BaseModel):
    status: str = Field(..., description="Service status", example="ok")
    service: str = Field(..., description="Service name", example="offerproof-api")
    version: str = Field(..., description="API Version", example="0.1.0")
    timestamp: datetime = Field(..., description="Current server UTC timestamp")
    environment: str = Field(..., description="Deployment environment", example="development")


class RootResponse(BaseModel):
    message: str = Field(..., description="Welcome greeting / platform description")
    tagline: str = Field(..., description="OFFERPROOF tagline")
    version: str = Field(..., description="API Version")
    docs_url: str = Field(..., description="API documentation URL")
    health_url: str = Field(..., description="API health endpoint URL")
