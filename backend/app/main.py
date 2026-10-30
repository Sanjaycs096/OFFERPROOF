import os
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from dotenv import load_dotenv

from app.schemas.health import RootResponse
from app.routes import api_router

# Load environment variables
load_dotenv()

app = FastAPI(
    title="OFFERPROOF API",
    description="Backend API for OFFERPROOF: AI-assisted, evidence-based opportunity verification platform.",
    version="0.1.0",
    docs_url="/docs",
    redoc_url="/redoc",
)

# Configure CORS origins
raw_origins = os.getenv(
    "CORS_ORIGINS",
    "http://localhost:5173,http://127.0.0.1:5173,http://localhost:3000",
)
allowed_origins = [origin.strip() for origin in raw_origins.split(",") if origin.strip()]

app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Global error handler
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    return JSONResponse(
        status_code=500,
        content={
            "error": "InternalServerError",
            "message": "An unexpected error occurred while processing the request.",
            "detail": str(exc) if os.getenv("ENVIRONMENT") == "development" else None,
        },
    )

# Include modular routes
app.include_router(api_router)


@app.get("/", response_model=RootResponse, tags=["General"])
def root_info() -> RootResponse:
    """
    Returns platform metadata and quick API navigation links.
    """
    return RootResponse(
        message="OFFERPROOF API is active and ready.",
        tagline="Don't trust the offer. Verify the evidence.",
        version="0.1.0",
        docs_url="/docs",
        health_url="/health",
    )


if __name__ == "__main__":
    import uvicorn

    port = int(os.getenv("PORT", 8000))
    host = os.getenv("HOST", "0.0.0.0")
    uvicorn.run("app.main:app", host=host, port=port, reload=True)
