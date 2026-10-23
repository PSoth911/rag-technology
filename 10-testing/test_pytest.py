"""
=============================================================================
RAG Technology Testing Lab — Technology 22: pytest Test Automation
=============================================================================

1. TECHNOLOGY OVERVIEW:
   pytest is the standard test runner and automation framework for Python.
   In our RAG pipeline, pytest enables:
   - Automated regression testing across data transformation steps.
   - Verifying multilingual character preservation and Unicode normalization.
   - Asserting API endpoint status codes, schemas, and citation formats.
   - Boundary condition testing for chunking algorithms and token limits.

2. INSTALLATION / PREREQUISITES:
   pip install pytest httpx

3. EXECUTION INSTRUCTIONS:
   .\\.venv\\Scripts\\pytest 10-testing/test_pytest.py -v
   Or:
   py -m pytest 10-testing/test_pytest.py -v

=============================================================================
"""

import sys
import unicodedata
from pathlib import Path
import pytest

# Ensure parent directory is in sys.path
root_dir = Path(__file__).resolve().parent.parent
backend_dir = root_dir / "02-backend"
prog_dir = root_dir / "01-programming"

for p in (root_dir, backend_dir, prog_dir):
    if str(p) not in sys.path:
        sys.path.insert(0, str(p))

from test_fastapi import app, QueryRequest
from test_pydantic import RAGQueryRequest, Citation
from test_python import sliding_window_chunker, detect_language_simple


# =============================================================================
# UNIT TESTS
# =============================================================================

def test_khmer_unicode_nfc_normalization():
    """Verify that Khmer text containing combining marks normalizes properly."""
    raw_khmer = "ប្រព័ន្ធស្វែងរក និងបង្កើតព័ត៌មាន (RAG)"
    normalized = unicodedata.normalize("NFC", raw_khmer)
    assert len(normalized) > 0
    assert any("\u1780" <= c <= "\u17ff" for c in normalized)
    assert "RAG" in normalized


def test_sliding_window_chunker_overlap():
    """Verify that sliding window generator creates overlapping chunks correctly."""
    sample_corpus = "Sentence one. Sentence two. Sentence three. Sentence four. Sentence five."
    chunks = list(sliding_window_chunker(sample_corpus, doc_id="DOC-TEST", page_number=1, chunk_size=35, chunk_overlap=10))

    assert len(chunks) >= 2
    # Verify sequential chunk IDs
    assert chunks[0].chunk_id == "DOC-TEST-p1-c000"
    assert chunks[1].chunk_id == "DOC-TEST-p1-c001"
    # Verify metadata offsets
    assert chunks[0].metadata["start_char"] == 0
    assert chunks[1].metadata["start_char"] == 25  # step = 35 - 10


def test_language_detection_heuristics():
    """Verify simple language categorization on English, Khmer, and mixed inputs."""
    assert detect_language_simple("Retrieval-Augmented Generation") == "en"
    assert detect_language_simple("ប្រព័ន្ធស្វែងរក និងបង្កើតព័ត៌មាន") == "km"
    assert detect_language_simple("RAG គឺជាស្ថាបត្យកម្ម") in ("km", "mixed")


def test_pydantic_query_validation():
    """Verify Pydantic schema constraints on query string length and top_k bounds."""
    # Valid
    req = RAGQueryRequest(question="What is pgvector?", top_k=5, language="en")
    assert req.question == "What is pgvector?"
    assert req.top_k == 5

    # Invalid - question too short
    with pytest.raises(Exception):
        RAGQueryRequest(question="a", top_k=5)

    # Invalid - top_k exceeds bound
    with pytest.raises(Exception):
        RAGQueryRequest(question="Valid question", top_k=999)


def test_citation_data_structure():
    """Verify citation model integrity."""
    cit = Citation(
        doc_id="DOC-2026",
        page_number=3,
        chunk_id="DOC-2026-p3-c002",
        snippet="Authoritative passage from knowledge base."
    )
    assert cit.doc_id == "DOC-2026"
    assert cit.page_number == 3
    assert "Authoritative" in cit.snippet


def test_fastapi_health_endpoint():
    """Verify FastAPI GET /health via Starlette TestClient."""
    from fastapi.testclient import TestClient
    client = TestClient(app)
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    assert data["service"] == "rag-technology-lab"


def test_fastapi_khmer_query_endpoint():
    """Verify FastAPI POST /api/query returns citations for Khmer questions."""
    from fastapi.testclient import TestClient
    client = TestClient(app)
    response = client.post("/api/query", json={
        "question": "តើប្រព័ន្ធ RAG ជួយអ្វីខ្លះ?",
        "top_k": 3,
        "language": "km"
    })
    assert response.status_code == 200
    data = response.json()
    assert "citations" in data
    assert len(data["citations"]) > 0
    assert "DOC-KM-01" in data["citations"][0]["doc_id"]
