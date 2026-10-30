import asyncio
import sys
from pathlib import Path

# Add backend directory to sys.path
backend_dir = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(backend_dir))

from httpx import ASGITransport, AsyncClient
from app.main import app


async def run_tests():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://testserver") as client:
        # Test Root Endpoint
        res_root = await client.get("/")
        print("Root Status:", res_root.status_code)
        print("Root Response:", res_root.json())
        assert res_root.status_code == 200
        root_data = res_root.json()
        assert "message" in root_data
        assert root_data["tagline"] == "Don't trust the offer. Verify the evidence."
        assert root_data["health_url"] == "/health"
        assert root_data["docs_url"] == "/docs"

        # Test Health Endpoint
        res_health = await client.get("/health")
        print("\nHealth Status:", res_health.status_code)
        print("Health Response:", res_health.json())
        assert res_health.status_code == 200
        health_data = res_health.json()
        assert health_data["status"] == "ok"
        assert health_data["service"] == "offerproof-api"
        assert health_data["version"] == "0.1.0"
        assert "timestamp" in health_data

        # Test CORS Preflight
        res_cors = await client.options(
            "/health",
            headers={
                "Origin": "http://localhost:5173",
                "Access-Control-Request-Method": "GET",
            },
        )
        print("\nCORS Status:", res_cors.status_code)
        print("CORS Origin Header:", res_cors.headers.get("access-control-allow-origin"))
        assert res_cors.status_code == 200
        assert res_cors.headers.get("access-control-allow-origin") == "http://localhost:5173"

    print("\n[PASS] ALL BACKEND TESTS PASSED SUCCESSFULLY!")


if __name__ == "__main__":
    asyncio.run(run_tests())
