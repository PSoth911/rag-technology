"""
=============================================================================
RAG Technology Testing Lab — Technology 01: Python 3.12
=============================================================================

1. TECHNOLOGY OVERVIEW:
   Python 3.12 serves as the core programming language foundation for the RAG
   pipeline. It provides standard library primitives for data structures,
   type hinting, memory-efficient generators, structured dataclasses, and
   robust UTF-8 Unicode processing required to ingest, chunk, and index
   multilingual text (both English and Khmer).

2. INSTALLATION / PREREQUISITES:
   - Python 3.12+ (or 3.13) installed on Windows 11.
   - No external pip dependencies required. This test uses the Python standard
     library exclusively (pathlib, json, hashlib, dataclasses, unicodedata, typing).

3. EXECUTION INSTRUCTIONS:
   From the repository root (`ragTechTest/`):
     py 01-programming/test_python.py
   Or with an active virtual environment:
     python 01-programming/test_python.py

=============================================================================
"""

from __future__ import annotations

import hashlib
import json
import os
import sys
import unicodedata
from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import Generator, Sequence

# Windows console UTF-8 fix: default Windows cmd/powershell uses cp1252
if sys.platform == "win32":
    try:
        if hasattr(sys.stdout, "reconfigure"):
            sys.stdout.reconfigure(encoding="utf-8", errors="replace")
        if hasattr(sys.stderr, "reconfigure"):
            sys.stderr.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass


# =============================================================================
# 1. DATA STRUCTURES & TYPING FOR RAG
# =============================================================================

@dataclass(slots=True, kw_only=True)
class DocumentChunk:
    """Represents an atomic text chunk extracted from a source document."""
    chunk_id: str
    doc_id: str
    page_number: int
    text: str
    char_count: int
    language: str
    metadata: dict[str, str | int] = field(default_factory=dict)


@dataclass(slots=True, kw_only=True)
class IngestionReport:
    """Summary of the document ingestion and chunking outcome."""
    doc_id: str
    total_characters: int
    total_chunks: int
    languages_detected: list[str]
    checksum_sha256: str


# =============================================================================
# 2. CORE FUNCTIONS
# =============================================================================

def compute_document_hash(raw_text: str) -> str:
    """
    Computes a SHA-256 fingerprint of the raw text.
    Used in RAG pipelines to prevent redundant re-indexing and detect revisions.
    """
    return hashlib.sha256(raw_text.encode("utf-8")).hexdigest()


def detect_language_simple(text: str) -> str:
    """
    Detects whether a snippet is predominantly Khmer, English, or Mixed
    by inspecting Unicode script proportions.
    Khmer Unicode block: U+1780 to U+17FF.
    Gracefully handles English technical acronyms (e.g. 'RAG', 'AI') embedded in Khmer text.
    """
    khmer_count = sum(1 for ch in text if "\u1780" <= ch <= "\u17ff")
    ascii_count = sum(1 for ch in text if ch.isascii() and ch.isalpha())
    total_letters = khmer_count + ascii_count

    if total_letters == 0:
        return "unknown"

    khmer_ratio = khmer_count / total_letters
    ascii_ratio = ascii_count / total_letters

    if khmer_ratio >= 0.70:
        return "km"
    elif ascii_ratio >= 0.70:
        return "en"
    elif khmer_count > 0 and ascii_count > 0:
        return "mixed"
    else:
        return "unknown"


def sliding_window_chunker(
    text: str,
    doc_id: str,
    page_number: int,
    chunk_size: int = 120,
    chunk_overlap: int = 30,
) -> Generator[DocumentChunk, None, None]:
    """
    Splits text into overlapping sliding-window chunks.
    Yields chunks lazily via a generator to ensure minimal memory usage during
    large document ingestion.
    """
    if chunk_size <= chunk_overlap:
        raise ValueError("chunk_size must be strictly greater than chunk_overlap.")

    # Normalize unicode to NFC to handle Khmer composite vowels & diacritics
    normalized_text = unicodedata.normalize("NFC", text.strip())
    step = chunk_size - chunk_overlap
    text_len = len(normalized_text)
    chunk_idx = 0

    for start_idx in range(0, text_len, step):
        end_idx = min(start_idx + chunk_size, text_len)
        chunk_slice = normalized_text[start_idx:end_idx]

        if not chunk_slice.strip():
            continue

        chunk_id = f"{doc_id}-p{page_number}-c{chunk_idx:03d}"
        lang = detect_language_simple(chunk_slice)

        yield DocumentChunk(
            chunk_id=chunk_id,
            doc_id=doc_id,
            page_number=page_number,
            text=chunk_slice,
            char_count=len(chunk_slice),
            language=lang,
            metadata={"start_char": start_idx, "end_char": end_idx},
        )
        chunk_idx += 1

        if end_idx >= text_len:
            break


def save_and_verify_json(
    chunks: Sequence[DocumentChunk],
    destination_path: Path,
) -> bool:
    """
    Serializes chunks to JSON with UTF-8 encoding (ensure_ascii=False)
    so Khmer script characters are stored natively, then validates reload.
    """
    destination_path.parent.mkdir(parents=True, exist_ok=True)
    serialized = [asdict(chunk) for chunk in chunks]

    # Write UTF-8 JSON file
    with open(destination_path, "w", encoding="utf-8") as f:
        json.dump(serialized, f, ensure_ascii=False, indent=2)

    # Reload and verify integrity
    with open(destination_path, "r", encoding="utf-8") as f:
        reloaded = json.load(f)

    return len(reloaded) == len(chunks)


# =============================================================================
# 3. SAMPLE INPUTS (ENGLISH & KHMER)
# =============================================================================

SAMPLE_ENGLISH_TEXT = (
    "Retrieval-Augmented Generation (RAG) optimizes the output of an LLM by "
    "referencing an authoritative knowledge base outside of its training data "
    "before generating a response. This reduces hallucinations and provides citations."
)

SAMPLE_KHMER_TEXT = (
    "ប្រព័ន្ធស្វែងរក និងបង្កើតព័ត៌មាន (RAG) ជួយបង្កើនគុណភាពនៃចម្លើយរបស់បញ្ញាសិប្បនិម្មិត "
    "ដោយទាញយកទិន្នន័យជាក់លាក់ពីឯកសារយោង និងទប់ស្កាត់ការឆ្លើយខុសពីការពិត។"
)


# =============================================================================
# 4. TEST EXECUTION & EVALUATION
# =============================================================================

def run_test() -> bool:
    print("=" * 70)
    print("🧪 Running 01-programming: Python 3.12 Fundamentals Test")
    print("=" * 70)
    print(f"• Python Version : {sys.version.split()[0]} ({sys.platform})")
    print(f"• Default Encoding: {sys.getdefaultencoding()}")

    all_tests_passed = True

    # Test 1: Multilingual Unicode & Khmer diacritics normalization
    print("\n[Step 1/5] Testing UTF-8 and Khmer Unicode Normalization...")
    norm_en = unicodedata.normalize("NFC", SAMPLE_ENGLISH_TEXT)
    norm_km = unicodedata.normalize("NFC", SAMPLE_KHMER_TEXT)
    print(f"  ✓ English length : {len(norm_en)} characters")
    print(f"  ✓ Khmer length   : {len(norm_km)} characters")
    print(f"  ✓ Sample Khmer   : {norm_km[:40]}...")

    if len(norm_km) == 0 or not any("\u1780" <= c <= "\u17ff" for c in norm_km):
        print("  ✗ Khmer Unicode processing failed.")
        all_tests_passed = False
    else:
        print("  ✓ Unicode normalization passed.")

    # Test 2: SHA-256 Document Hashing (Deduplication)
    print("\n[Step 2/5] Testing Document Deduplication Hash (SHA-256)...")
    hash_en = compute_document_hash(SAMPLE_ENGLISH_TEXT)
    hash_km = compute_document_hash(SAMPLE_KHMER_TEXT)
    print(f"  ✓ English Doc Hash: {hash_en[:16]}...{hash_en[-8:]}")
    print(f"  ✓ Khmer Doc Hash  : {hash_km[:16]}...{hash_km[-8:]}")
    assert len(hash_en) == 64 and len(hash_km) == 64, "Hash output must be 64 hex characters"
    print("  ✓ SHA-256 fingerprinting passed.")

    # Test 3: Language Detection via Pattern Matching
    print("\n[Step 3/5] Testing Pattern Matching & Language Detection...")
    lang_en = detect_language_simple(SAMPLE_ENGLISH_TEXT)
    lang_km = detect_language_simple(SAMPLE_KHMER_TEXT)
    print(f"  ✓ Detected English snippet as: '{lang_en}' (expected 'en')")
    print(f"  ✓ Detected Khmer snippet as  : '{lang_km}' (expected 'km')")
    if lang_en != "en" or lang_km != "km":
        print("  ✗ Language detection mismatch.")
        all_tests_passed = False
    else:
        print("  ✓ Language detection passed.")

    # Test 4: Sliding Window Chunking Generator
    print("\n[Step 4/5] Testing Sliding Window Chunking (Generator)...")
    combined_corpus = f"{SAMPLE_ENGLISH_TEXT}\n\n{SAMPLE_KHMER_TEXT}"
    chunks: list[DocumentChunk] = list(
        sliding_window_chunker(
            text=combined_corpus,
            doc_id="DOC-2026-001",
            page_number=1,
            chunk_size=100,
            chunk_overlap=25,
        )
    )
    print(f"  ✓ Generated {len(chunks)} chunks from combined multilingual input.")
    for idx, c in enumerate(chunks[:3]):
        print(f"    - Chunk [{idx}] ({c.chunk_id}, lang={c.language}): {c.text[:45]}...")

    if len(chunks) < 2:
        print("  ✗ Expected at least 2 chunks, got fewer.")
        all_tests_passed = False
    else:
        print("  ✓ Sliding window chunker passed.")

    # Test 5: JSON UTF-8 Persistence & Verification
    print("\n[Step 5/5] Testing JSON Persistence (Khmer Script Preserved)...")
    output_file = Path(__file__).resolve().parent / "output" / "sample_chunks.json"
    success = save_and_verify_json(chunks, output_file)
    print(f"  ✓ Saved to: {output_file.name}")
    print(f"  ✓ File size: {output_file.stat().st_size} bytes")
    print(f"  ✓ Verification status: {'PASSED' if success else 'FAILED'}")

    # Inspect that raw file contains non-escaped Khmer
    with open(output_file, "r", encoding="utf-8") as f:
        file_content = f.read()
        has_raw_khmer = "ប្រព័ន្ធ" in file_content
        print(f"  ✓ Raw Khmer characters unescaped: {has_raw_khmer}")

    if not (success and has_raw_khmer):
        all_tests_passed = False

    # Summary
    print("\n" + "=" * 70)
    if all_tests_passed:
        print("🎉 SUCCESS: Python 3.12 technology test passed all evaluations!")
    else:
        print("❌ FAILURE: One or more test steps failed.")
    print("=" * 70)
    return all_tests_passed


if __name__ == "__main__":
    test_result = run_test()
    sys.exit(0 if test_result else 1)
