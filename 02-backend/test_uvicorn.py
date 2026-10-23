"""
=============================================================================
RAG Technology Testing Lab — Technology 04: Uvicorn ASGI Server
=============================================================================

1. TECHNOLOGY OVERVIEW:
   Uvicorn is an ASGI (Asynchronous Server Gateway Interface) web server
   implementation for Python. It executes asynchronous Python frameworks
   (FastAPI / Starlette) with event loops (asyncio / uvloop), handling
   concurrent HTTP/1.1 and WebSocket connections. In our RAG system, Uvicorn
   powers the real-time inference server handling document queries and streaming tokens.

2. INSTALLATION:
   pip install uvicorn[standard]

3. EXECUTION INSTRUCTIONS:
   # Run the automated programmatic server lifecycle test:
   .\\.venv\\Scripts\\python 02-backend/test_uvicorn.py

   # Or launch directly with CLI for continuous development:
   .\\.venv\\Scripts\\uvicorn 02-backend.test_fastapi:app --host 127.0.0.1 --port 8000 --reload
=============================================================================
"""

from __future__ import annotations

import asyncio
import sys
import threading
import time
from pathlib import Path
import httpx
import uvicorn

# Windows console UTF-8 fix
if sys.platform == "win32":
    try:
        if hasattr(sys.stdout, "reconfigure"):
            sys.stdout.reconfigure(encoding="utf-8", errors="replace")
        if hasattr(sys.stderr, "reconfigure"):
            sys.stderr.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

# Ensure local backend modules can be imported
backend_dir = Path(__file__).resolve().parent
if str(backend_dir) not in sys.path:
    sys.path.insert(0, str(backend_dir))

from test_fastapi import app  # noqa: E402

HOST = "127.0.0.1"
PORT = 8008  # Use a dedicated port to prevent collisions


def run_test() -> bool:
    print("=" * 70)
    print("🧪 Running 02-backend: Uvicorn ASGI Server Lifecycle Test")
    print("=" * 70)
    print(f"• Target Endpoint: http://{HOST}:{PORT}/health")

    config = uvicorn.Config(
        app=app,
        host=HOST,
        port=PORT,
        log_level="warning",
        loop="asyncio",
    )
    server = uvicorn.Server(config)

    # Run Uvicorn in a background thread so we can test it from the main thread
    server_thread = threading.Thread(target=server.run, daemon=True)
    server_thread.start()

    all_passed = True
    print("\n[Step 1/3] Waiting for Uvicorn server to bind and start...")

    # Wait up to 5 seconds for the socket to accept connections
    started = False
    for _ in range(25):
        if server.started:
            started = True
            break
        time.sleep(0.1)

    if not started:
        print("  ✗ Server failed to start within timeout.")
        server.should_exit = True
        return False

    print("  ✓ Uvicorn server is running in background thread.")

    # Test live HTTP communication
    print("\n[Step 2/3] Sending live HTTP GET request to Uvicorn...")
    try:
        with httpx.Client(timeout=3.0) as client:
            resp = client.get(f"http://{HOST}:{PORT}/health")
            print(f"  ✓ Response Status: {resp.status_code}")
            print(f"  ✓ Response Payload: {resp.json()}")
            assert resp.status_code == 200
            assert resp.json().get("status") == "healthy"
            print("  ✓ Live HTTP communication verified successfully.")
    except Exception as exc:
        print(f"  ✗ Failed to connect to Uvicorn: {exc}")
        all_passed = False

    # Graceful shutdown
    print("\n[Step 3/3] Triggering graceful server shutdown...")
    server.should_exit = True
    server_thread.join(timeout=4.0)

    if not server_thread.is_alive():
        print("  ✓ Uvicorn server stopped cleanly.")
    else:
        print("  ⚠ Server thread did not terminate within timeout.")
        all_passed = False

    print("\n" + "=" * 70)
    if all_passed:
        print("🎉 SUCCESS: Uvicorn technology test passed all evaluations!")
    else:
        print("❌ FAILURE: Uvicorn test encountered issues.")
    print("=" * 70)
    return all_passed


if __name__ == "__main__":
    success = run_test()
    sys.exit(0 if success else 1)
