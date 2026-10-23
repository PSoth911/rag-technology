"""
=============================================================================
RAG Technology Testing Lab — Technology 03: Pydantic v2
=============================================================================

1. TECHNOLOGY OVERVIEW:
   Pydantic provides high-performance data validation and serialization
   using standard Python type annotations. In a RAG pipeline, Pydantic ensures:
   - Inbound search queries, top_k limits, and filters are strictly valid.
   - Multilingual document payloads (Khmer & English) conform to expected schemas.
   - LLM generation responses, citations, and metadata dictionaries are strictly typed.

2. INSTALLATION / PREREQUISITES:
   pip install pydantic

3. EXECUTION INSTRUCTIONS:
   .\\.venv\\Scripts\\python 02-backend/test_pydantic.py
   Or:
   py 02-backend/test_pydantic.py (with dependencies installed)

=============================================================================
"""

from __future__ import annotations

import json
import sys
from typing import Any, Literal
from pydantic import BaseModel, Field, ValidationError, field_validator, ConfigDict

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
# 1. RAG SCHEMAS & MODELS
# =============================================================================

class Citation(BaseModel):
    """Represents a verifiable citation back to source documents."""
    model_config = ConfigDict(frozen=True)

    doc_id: str = Field(..., description="Unique document ID (e.g. DOC-2026-001)")
    page_number: int = Field(..., ge=1, description="1-indexed source document page")
    chunk_id: str = Field(..., description="Unique chunk reference identifier")
    snippet: str = Field(..., min_length=5, description="Exact cited excerpt")


class RAGQueryRequest(BaseModel):
    """Search & QA request submitted by users or frontend clients."""
    question: str = Field(..., min_length=3, max_length=1000, description="User search query in English or Khmer")
    top_k: int = Field(default=5, ge=1, le=50, description="Number of context chunks to retrieve")
    language: Literal["en", "km", "auto"] = Field(default="auto", description="Target language context")
    metadata_filter: dict[str, Any] = Field(default_factory=dict, description="Metadata filtering predicates")

    @field_validator("question")
    @classmethod
    def strip_and_validate_question(cls, v: str) -> str:
        cleaned = v.strip()
        if len(cleaned) < 3:
            raise ValueError("Question must be at least 3 non-whitespace characters long.")
        return cleaned


class RAGQueryResponse(BaseModel):
    """Full structured response returned by the RAG orchestrator."""
    query: str
    answer: str
    citations: list[Citation] = Field(default_factory=list)
    confidence_score: float = Field(..., ge=0.0, le=1.0)
    model_name: str
    latency_ms: int = Field(..., ge=0)


# =============================================================================
# 2. TEST EXECUTION & EVALUATION
# =============================================================================

def run_test() -> bool:
    print("=" * 70)
    print("🧪 Running 02-backend: Pydantic v2 Schema Validation Test")
    print("=" * 70)

    all_passed = True

    # Step 1: Valid English Query Validation
    print("\n[Step 1/4] Validating English RAG query request...")
    valid_en_payload = {
        "question": "What is the capital of Cambodia?",
        "top_k": 3,
        "language": "en",
        "metadata_filter": {"category": "geography"}
    }
    try:
        req_en = RAGQueryRequest.model_validate(valid_en_payload)
        print(f"  ✓ Validated successfully: question='{req_en.question}', top_k={req_en.top_k}")
    except ValidationError as e:
        print(f"  ✗ Validation error: {e}")
        all_passed = False

    # Step 2: Valid Khmer Query Validation & JSON serialization
    print("\n[Step 2/4] Validating Khmer query request & UTF-8 serialization...")
    valid_km_payload = {
        "question": "តើប្រព័ន្ធ RAG ដំណើរការយ៉ាងដូចម្តេច?",
        "top_k": 5,
        "language": "km"
    }
    try:
        req_km = RAGQueryRequest.model_validate(valid_km_payload)
        json_output = req_km.model_dump_json(indent=2)
        print(f"  ✓ Validated Khmer query: {req_km.question}")
        print(f"  ✓ Serialized length: {len(json_output)} bytes")
        assert "ដំណើរការ" in json_output
    except Exception as e:
        print(f"  ✗ Khmer validation failed: {e}")
        all_passed = False

    # Step 3: Complex Nested Response with Citations
    print("\n[Step 3/4] Validating nested RAG response with citations...")
    try:
        response = RAGQueryResponse(
            query="តើអ្វីជា RAG?",
            answer="RAG គឺជាស្ថាបត្យកម្មដែលរួមបញ្ចូលការស្វែងរកឯកសារយោងជាមួយនឹង LLM។",
            citations=[
                Citation(
                    doc_id="DOC-KM-001",
                    page_number=1,
                    chunk_id="DOC-KM-001-p1-c001",
                    snippet="ប្រព័ន្ធ RAG ជួយបង្កើនគុណភាពនៃចម្លើយរបស់បញ្ញាសិប្បនិម្មិត..."
                )
            ],
            confidence_score=0.96,
            model_name="qwen2.5:7b-instruct",
            latency_ms=342
        )
        print(f"  ✓ Response validated: {len(response.citations)} citation(s) attached.")
        print(f"  ✓ Model: {response.model_name}, Latency: {response.latency_ms}ms")
    except ValidationError as e:
        print(f"  ✗ Nested model validation error: {e}")
        all_passed = False

    # Step 4: Invalid Payload Handling & Error Reporting
    print("\n[Step 4/4] Testing boundary rejections & error reporting...")
    invalid_payload = {
        "question": "  ",      # Too short / whitespace
        "top_k": 999,          # Exceeds le=50
        "language": "spanish"  # Not in allowed Literal
    }
    try:
        RAGQueryRequest.model_validate(invalid_payload)
        print("  ✗ Expected ValidationError was NOT raised!")
        all_passed = False
    except ValidationError as exc:
        errors = exc.errors()
        print(f"  ✓ Successfully caught {len(errors)} validation error(s) as expected:")
        for err in errors:
            loc = ".".join(str(x) for x in err["loc"])
            print(f"    - Field '{loc}': {err['msg']} (type={err['type']})")

    print("\n" + "=" * 70)
    if all_passed:
        print("🎉 SUCCESS: Pydantic v2 technology test passed all evaluations!")
    else:
        print("❌ FAILURE: One or more test steps failed.")
    print("=" * 70)
    return all_passed


if __name__ == "__main__":
    success = run_test()
    sys.exit(0 if success else 1)
