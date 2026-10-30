import subprocess
import time
import sys
import urllib.request
import json

def test_live_server():
    python_exe = sys.executable
    print(f"Starting uvicorn server with {python_exe}...")
    proc = subprocess.Popen(
        [python_exe, "-m", "uvicorn", "app.main:app", "--host", "127.0.0.1", "--port", "8000"],
        cwd="backend",
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )

    try:
        # Give server time to bind and listen
        time.sleep(2.5)

        # 1. Test Root Endpoint
        req_root = urllib.request.Request("http://127.0.0.1:8000/")
        with urllib.request.urlopen(req_root, timeout=5) as res:
            assert res.status == 200
            data = json.loads(res.read().decode())
            print("[PASS] HTTP Live Server Root GET /:", data)

        # 2. Test Health Endpoint
        req_health = urllib.request.Request("http://127.0.0.1:8000/health")
        with urllib.request.urlopen(req_health, timeout=5) as res:
            assert res.status == 200
            data = json.loads(res.read().decode())
            print("[PASS] HTTP Live Server Health GET /health:", data)

        print("\n[SUCCESS] Live Uvicorn server successfully bound to port 8000 and answered requests!")
    finally:
        print("Stopping uvicorn server...")
        proc.terminate()
        try:
            proc.wait(timeout=3)
        except subprocess.TimeoutExpired:
            proc.kill()
        print("Server stopped cleanly.")

if __name__ == "__main__":
    test_live_server()
