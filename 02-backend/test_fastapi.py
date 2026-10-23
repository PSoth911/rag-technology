"""
=============================================================================
RAG Technology Testing Lab — Technology 02: FastAPI
=============================================================================

1. TECHNOLOGY OVERVIEW:
   FastAPI is a modern, high-performance web framework for building APIs with
   Python 3.8+ based on standard Python type hints and OpenAPI standards.
   In a RAG system, FastAPI serves as the gateway for:
   - Client query ingestion and validation.
   - Document chunk submission and indexing triggers.
   - Streaming LLM generation responses and formatted citations to frontend UIs.

2. INSTALLATION / PREREQUISITES:
   pip install fastapi uvicorn[standard] httpx

3. EXECUTION INSTRUCTIONS:
   # Run the automated endpoint tests:
   .\\.venv\\Scripts\\python 02-backend/test_fastapi.py

   # Or run the live development server with auto-docs:
   .\\.venv\\Scripts\\python 02-backend/test_fastapi.py --serve
   # Then visit: http://127.0.0.1:8000/docs
=============================================================================
"""

from __future__ import annotations

import sys
import time
from typing import Any, Literal
from fastapi import FastAPI, HTTPException, status
from fastapi.testclient import TestClient
from pydantic import BaseModel, Field

# Windows console UTF-8 fix
if sys.platform == "win32":
    try:
        if hasattr(sys.stdout, "reconfigure"):
            sys.stdout.reconfigure(encoding="utf-8", errors="replace")
        if hasattr(sys.stderr, "reconfigure"):
            sys.stderr.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass


# =============================================================================
# 1. API SCHEMAS
# =============================================================================

class HealthResponse(BaseModel):
    status: str
    service: str
    version: str
    timestamp: float


class IngestChunkPayload(BaseModel):
    chunk_id: str
    doc_id: str
    page_number: int = Field(..., ge=1)
    text: str = Field(..., min_length=1)
    language: str = "en"


class IngestResponse(BaseModel):
    message: str
    chunks_indexed: int
    doc_id: str


class CitationItem(BaseModel):
    doc_id: str
    page_number: int
    chunk_id: str
    snippet: str


class QueryRequest(BaseModel):
    question: str = Field(..., min_length=3, max_length=1000)
    top_k: int = Field(default=3, ge=1, le=20)
    language: Literal["en", "km", "auto"] = "auto"


class QueryResponse(BaseModel):
    query: str
    answer: str
    citations: list[CitationItem]
    top_k: int
    latency_ms: int


# =============================================================================
# 2. FASTAPI APPLICATION SETUP
# =============================================================================

app = FastAPI(
    title="RAG Technology Lab API",
    description="Backend API testing endpoints for document retrieval, chunk ingestion, and multilingual Q&A.",
    version="1.0.0",
)

# Simulated in-memory vector/chunk store for testing
_CHUNK_STORE: dict[str, IngestChunkPayload] = {}


@app.get("/health", response_model=HealthResponse, tags=["System"])
async def health_check():
    """Returns service health status and timestamp."""
    return HealthResponse(
        status="healthy",
        service="rag-technology-lab",
        version="1.0.0",
        timestamp=time.time(),
    )


@app.post("/api/chunks", response_model=IngestResponse, status_code=status.HTTP_201_CREATED, tags=["Ingestion"])
async def ingest_chunks(chunks: list[IngestChunkPayload]):
    """Ingests document chunks for vector indexing."""
    if not chunks:
        raise HTTPException(status_code=400, detail="Chunk list cannot be empty.")

    doc_ids = set()
    for chunk in chunks:
        _CHUNK_STORE[chunk.chunk_id] = chunk
        doc_ids.add(chunk.doc_id)

    return IngestResponse(
        message="Chunks received and indexed successfully.",
        chunks_indexed=len(chunks),
        doc_id=", ".join(doc_ids),
    )


@app.post("/api/query", response_model=QueryResponse, tags=["Retrieval & QA"])
async def query_rag(req: QueryRequest):
    """Answers user queries in English or Khmer with document citations."""
    start_time = time.perf_counter()

    # Determine simulated answer based on language/content
    is_khmer = any("\u1780" <= c <= "\u17ff" for c in req.question)

    if is_khmer:
        answer = "ប្រព័ន្ធ RAG ជួយបង្កើនសមត្ថភាពឆ្លើយសំណួររបស់ AI ដោយផ្អែកលើឯកសារយោងជាក់លាក់។"
        citations = [
            CitationItem(
                doc_id="DOC-KM-01",
                page_number=1,
                chunk_id="DOC-KM-01-p1-c001",
                snippet="ឯកសារស្តីពីបច្ចេកវិទ្យាបញ្ញាសិប្បនិម្មិត និងប្រព័ន្ធស្វែងរកទិន្នន័យ។",
            )
        ]
    else:
        answer = "Retrieval-Augmented Generation synthesizes verified context to generate grounded answers."
        citations = [
            CitationItem(
                doc_id="DOC-EN-01",
                page_number=1,
                chunk_id="DOC-EN-01-p1-c001",
                snippet="RAG grounds model responses on retrieved authoritative document passages.",
            )
        ]

    latency_ms = int((time.perf_counter() - start_time) * 1000)

    return QueryResponse(
        query=req.question,
        answer=answer,
        citations=citations,
        top_k=req.top_k,
        latency_ms=latency_ms,
    )


# =============================================================================
# 3. TEST SUITE (Self-contained via TestClient)
# =============================================================================

def run_test() -> bool:
    print("=" * 70)
    print("🧪 Running 02-backend: FastAPI Endpoints Test")
    print("=" * 70)

    client = TestClient(app)
    all_passed = True

    # Test 1: GET /health
    print("\n[Step 1/4] Testing GET /health endpoint...")
    resp = client.get("/health")
    print(f"  ✓ Status code: {resp.status_code}")
    if resp.status_code == 200 and resp.json().get("status") == "healthy":
        print("  ✓ Health check passed.")
    else:
        print(f"  ✗ Health check failed: {resp.text}")
        all_passed = False

    # Test 2: POST /api/chunks (Ingest multilingual chunk)
    print("\n[Step 2/4] Testing POST /api/chunks ingestion...")
    sample_chunk = [
        {
            "chunk_id": "CHUNK-KM-001",
            "doc_id": "DOC-KHMER-101",
            "page_number": 2,
            "text": "ឯកសារស្រាវជ្រាវអំពីការអភិវឌ្ឍន៍សេដ្ឋកិច្ចកម្ពុជា",
            "language": "km",
        }
    ]
    resp = client.post("/api/chunks", json=sample_chunk)
    print(f"  ✓ Status code: {resp.status_code}")
    if resp.status_code == 201 and resp.json().get("chunks_indexed") == 1:
        print(f"  ✓ Chunk ingestion passed: {resp.json()['message']}")
    else:
        print(f"  ✗ Ingestion failed: {resp.text}")
        all_passed = False

    # Test 3: POST /api/query (Khmer Query with Citations)
    print("\n[Step 3/4] Testing POST /api/query (Khmer Query & Citations)...")
    km_query = {
        "question": "តើប្រព័ន្ធ RAG ជួយអ្វីខ្លះ?",
        "top_k": 3,
        "language": "km",
    }
    resp = client.post("/api/query", json=km_query)
    print(f"  ✓ Status code: {resp.status_code}")
    data = resp.json()
    if resp.status_code == 200 and "citations" in data and len(data["citations"]) > 0:
        print(f"  ✓ Answer: {data['answer']}")
        print(f"  ✓ Citations count: {len(data['citations'])}")
        print(f"  ✓ First citation doc_id: {data['citations'][0]['doc_id']}")
    else:
        print(f"  ✗ Query endpoint failed: {resp.text}")
        all_passed = False

    # Test 4: Validation Error Handling (422 Unprocessable Entity)
    print("\n[Step 4/4] Testing validation error on malformed input (422)...")
    bad_req = {"question": "ab", "top_k": 999}  # min_length=3, top_k le=20
    resp = client.post("/api/query", json=bad_req)
    print(f"  ✓ Status code: {resp.status_code} (Expected 422)")
    if resp.status_code == 422:
        print("  ✓ Automatic 422 validation rejection confirmed.")
    else:
        print(f"  ✗ Expected 422, got {resp.status_code}")
        all_passed = False

    print("\n" + "=" * 70)
    if all_passed:
        print("🎉 SUCCESS: FastAPI technology test passed all evaluations!")
    else:
        print("❌ FAILURE: One or more test steps failed.")
    print("=" * 70)
    return all_passed


if __name__ == "__main__":
    if "--serve" in sys.argv:
        import uvicorn
        print("Starting FastAPI live server on http://127.0.0.1:8000 ...")
        uvicorn.run("test_fastapi:app", host="127.0.0.1", port=8000, reload=True)
    else:
        success = run_test()
        sys.exit(0 if success else 1)
