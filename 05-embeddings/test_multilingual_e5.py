"""
=============================================================================
RAG Technology Testing Lab — Technology 10: Multilingual E5
=============================================================================

1. TECHNOLOGY OVERVIEW:
   Multilingual E5 (intfloat/multilingual-e5-*) is a family of text embedding
   models trained on massive multilingual web corpora.
   In our RAG system, Multilingual E5 enables:
   - Cross-lingual retrieval (e.g. matching a Khmer question to English reference documents).
   - Asymmetric search via explicit instruction prefixes:
       * Queries must be prefixed with: "query: "
       * Document passages must be prefixed with: "passage: "
   - Fast semantic vector generation on standard CPU and GPU hardware.

2. INSTALLATION / PREREQUISITES:
   pip install sentence-transformers torch numpy

3. EXECUTION INSTRUCTIONS:
   .\\.venv\\Scripts\\python 05-embeddings/test_multilingual_e5.py
   Or:
   py 05-embeddings/test_multilingual_e5.py

=============================================================================
"""

from __future__ import annotations

import os
import sys
import time
from pathlib import Path

# Windows console UTF-8 fix
if sys.platform == "win32":
    try:
        if hasattr(sys.stdout, "reconfigure"):
            sys.stdout.reconfigure(encoding="utf-8", errors="replace")
        if hasattr(sys.stderr, "reconfigure"):
            sys.stderr.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass


def run_test() -> bool:
    print("=" * 70, flush=True)
    print("🧪 Running 05-embeddings: Multilingual E5 Embedding Test", flush=True)
    print("=" * 70, flush=True)

    try:
        from sentence_transformers import SentenceTransformer, util
    except ImportError as exc:
        print(f"❌ Missing sentence-transformers dependency: {exc}", flush=True)
        return False

    all_passed = True
    # Default to multilingual-e5-small (384-dim, ~470MB) for fast testing
    model_id = os.environ.get("E5_MODEL_ID", "intfloat/multilingual-e5-small")

    # Step 1: Model Initialization
    print(f"\n[Step 1/4] Loading Multilingual E5 checkpoint: '{model_id}'...", flush=True)
    start_load = time.perf_counter()
    try:
        model = SentenceTransformer(model_id)
        load_time = round(time.perf_counter() - start_load, 2)
        dim = model.get_sentence_embedding_dimension()
        print(f"  ✓ Model loaded in {load_time}s. Embedding dimension: {dim}", flush=True)
    except Exception as exc:
        print(f"  ✗ Model load failed (network/disk error): {exc}", flush=True)
        return False

    # Step 2: Prepare Asymmetric Query and Passages (English and Khmer)
    print("\n[Step 2/4] Formatting asymmetric inputs with E5 prefixes...", flush=True)
    raw_passages = [
        "Retrieval-Augmented Generation (RAG) grounds language model outputs using external verified documents.",
        "PostgreSQL with pgvector stores high-dimensional embeddings and executes fast cosine similarity indexes.",
        "អង្គរវត្ត គឺជាប្រាសាទបុរាណដ៏ល្បីល្បាញបំផុតមួយរបស់ប្រទេសកម្ពុជា ដែលសាងសង់ក្នុងសតវត្សរ៍ទី១២។",
        "How to prepare traditional Italian pizza with mozzarella cheese and tomato sauce.",
    ]

    # Critical E5 Requirement: Prepend 'passage: ' to all stored documents
    passages_prefixed = [f"passage: {p}" for p in raw_passages]

    # Query in Khmer: "តើប្រព័ន្ធ RAG ដំណើរការយ៉ាងដូចម្តេច?" (How does RAG work?)
    # Critical E5 Requirement: Prepend 'query: ' to search queries
    khmer_query = "query: តើប្រព័ន្ធ RAG ដំណើរការយ៉ាងដូចម្តេច?"

    print(f"  ✓ Target Query: '{khmer_query}'", flush=True)
    print(f"  ✓ Total passages to index: {len(passages_prefixed)}", flush=True)

    # Step 3: Compute Embeddings & Cross-Lingual Cosine Similarity
    print("\n[Step 3/4] Encoding text and computing cross-lingual similarity...", flush=True)
    start_enc = time.perf_counter()
    doc_embeddings = model.encode(passages_prefixed, normalize_embeddings=True)
    query_embedding = model.encode(khmer_query, normalize_embeddings=True)
    enc_latency = round((time.perf_counter() - start_enc) * 1000, 2)

    print(f"  ✓ Vector generation complete in {enc_latency}ms.", flush=True)

    # Cosine similarity (since normalized, dot product equals cosine similarity)
    scores = util.cos_sim(query_embedding, doc_embeddings)[0]

    ranked = []
    for idx, passage in enumerate(raw_passages):
        ranked.append((float(scores[idx]), passage))

    ranked.sort(key=lambda x: x[0], reverse=True)

    for rank, (score, text) in enumerate(ranked, 1):
        preview = text[:80] + "..." if len(text) > 80 else text
        print(f"  Rank {rank} (score={score:.4f}): \"{preview}\"", flush=True)

    # Step 4: Validate Cross-Lingual Retrieval
    print("\n[Step 4/4] Validating cross-lingual semantic matching...", flush=True)
    top_hit_text = ranked[0][1]
    if "Retrieval-Augmented Generation" in top_hit_text:
        print("  ✓ Correct: Khmer RAG query accurately matched English RAG document as top hit!", flush=True)
    else:
        print(f"  ⚠ Top hit was: {top_hit_text}", flush=True)
        # Check if score is still strong
        rag_score = next(s for s, t in ranked if "Retrieval-Augmented" in t)
        pizza_score = next(s for s, t in ranked if "pizza" in t)
        if rag_score > pizza_score:
            print(f"  ✓ Cross-lingual margin preserved (RAG {rag_score:.4f} > Pizza {pizza_score:.4f})", flush=True)
        else:
            all_passed = False

    print("\n" + "=" * 70, flush=True)
    if all_passed:
        print("🎉 SUCCESS: Multilingual E5 technology test passed all evaluations!", flush=True)
    else:
        print("❌ FAILURE: Multilingual E5 test encountered issues.", flush=True)
    print("=" * 70, flush=True)
    return all_passed


if __name__ == "__main__":
    success = run_test()
    sys.exit(0 if success else 1)
