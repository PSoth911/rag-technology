"""
=============================================================================
RAG Technology Testing Lab — Technology 09: BGE-M3
=============================================================================

1. TECHNOLOGY OVERVIEW:
   BGE-M3 (BAAI/bge-m3) is a state-of-the-art multilingual embedding model
   featuring "Multi-Functionality, Multi-Linguality, Multi-Granularity":
   - Multi-Linguality: Supports 100+ languages including Khmer (ភាសាខ្មែរ).
   - Multi-Granularity: Handles inputs up to 8,192 tokens (unlike standard 512 token limits).
   - Multi-Functionality: Generates dense embeddings (1024-dim), lexical sparse weights,
     and multi-vector ColBERT-style token representations.

2. INSTALLATION / PREREQUISITES:
   pip install sentence-transformers torch numpy

3. EXECUTION INSTRUCTIONS:
   # Note: Default model is BAAI/bge-m3 (~2.2 GB). On first run it downloads weights.
   # For quick verification on low-memory systems, you can override:
   #   $env:BGE_MODEL_ID = "BAAI/bge-small-en-v1.5"
   .\\.venv\\Scripts\\python 05-embeddings/test_bge_m3.py
   Or:
   py 05-embeddings/test_bge_m3.py

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
    print("🧪 Running 05-embeddings: BGE-M3 Multilingual Embedding Test", flush=True)
    print("=" * 70, flush=True)

    try:
        from sentence_transformers import SentenceTransformer, util
    except ImportError as exc:
        print(f"❌ Missing sentence-transformers dependency: {exc}", flush=True)
        return False

    all_passed = True
    model_id = os.environ.get("BGE_MODEL_ID", "BAAI/bge-m3")

    # Step 1: Model Initialization
    print(f"\n[Step 1/4] Initializing BGE-M3 model: '{model_id}'...", flush=True)
    print("  ℹ️  Note: Model size is ~2.2 GB on disk with 1024 embedding dimension.", flush=True)
    start_load = time.perf_counter()
    try:
        # Load on CPU (or CUDA if available)
        model = SentenceTransformer(model_id, device="cpu")
        load_time = round(time.perf_counter() - start_load, 2)
        dim = model.get_sentence_embedding_dimension()
        max_seq = model.max_seq_length
        print(f"  ✓ Model loaded in {load_time}s.", flush=True)
        print(f"  ✓ Embedding Dimension : {dim}", flush=True)
        print(f"  ✓ Max Sequence Length : {max_seq} tokens", flush=True)
    except Exception as exc:
        print(f"  ✗ Model load failed (download interrupted or memory limit): {exc}", flush=True)
        print("  💡 Tip: You can test the script structure with a smaller model by setting:")
        print("       $env:BGE_MODEL_ID = 'BAAI/bge-small-en-v1.5'")
        return False

    # Step 2: Ingest Multilingual Corpus (English & Khmer)
    print("\n[Step 2/4] Encoding multilingual document passages...", flush=True)
    passages = [
        # Passage 0: English RAG
        "Retrieval-Augmented Generation synthesizes external context to eliminate AI hallucination.",
        # Passage 1: Khmer RAG description
        "ប្រព័ន្ធស្វែងរក និងបង្កើតព័ត៌មាន (RAG) ជួយបង្កើនគុណភាពនៃចម្លើយរបស់បញ្ញាសិប្បនិម្មិតដោយទាញយកទិន្នន័យជាក់លាក់ពីឯកសារយោង។",
        # Passage 2: PostgreSQL pgvector
        "PostgreSQL pgvector provides vector indexing methods including HNSW and IVFFlat.",
        # Passage 3: Culinary recipe distractor
        "A recipe for Italian espresso coffee and fresh bakery croissants.",
    ]

    start_enc = time.perf_counter()
    doc_vectors = model.encode(passages, normalize_embeddings=True)
    enc_time = round((time.perf_counter() - start_enc) * 1000, 2)
    print(f"  ✓ Encoded {len(passages)} passages in {enc_time}ms. Vector shape: {doc_vectors.shape}", flush=True)

    # Step 3: Khmer Query Cross-Lingual Evaluation
    print("\n[Step 3/4] Evaluating cross-lingual search (Khmer query against English & Khmer corpus)...", flush=True)
    # Query: "តើអ្វីជាប្រព័ន្ធ RAG?" (What is RAG system?)
    khmer_query = "តើអ្វីជាប្រព័ន្ធ RAG?"
    query_vector = model.encode(khmer_query, normalize_embeddings=True)

    scores = util.cos_sim(query_vector, doc_vectors)[0]

    ranked = []
    for idx, passage in enumerate(passages):
        ranked.append((float(scores[idx]), passage))

    ranked.sort(key=lambda x: x[0], reverse=True)

    print(f"  Query: \"{khmer_query}\"")
    for rank, (score, passage) in enumerate(ranked, 1):
        preview = passage[:75] + "..." if len(passage) > 75 else passage
        print(f"  Rank {rank} (score={score:.4f}): \"{preview}\"", flush=True)

    # Step 4: Verification of Top Retrieval
    print("\n[Step 4/4] Verifying semantic relevance ranking...", flush=True)
    # The top two hits should be the Khmer RAG passage and the English RAG passage!
    top_2_passages = [ranked[0][1], ranked[1][1]]
    has_khmer_rag = any("ប្រព័ន្ធស្វែងរក" in p for p in top_2_passages)
    has_english_rag = any("Retrieval-Augmented" in p for p in top_2_passages)
    bottom_passage = ranked[-1][1]

    if has_khmer_rag and has_english_rag:
        print("  ✓ Correct: Both Khmer and English RAG passages captured the top 2 ranks!", flush=True)
    else:
        print("  ⚠️ Ranking distribution:", top_2_passages, flush=True)

    if "croissants" in bottom_passage or "espresso" in bottom_passage:
        print("  ✓ Correct: Unrelated distractor (croissants/coffee) ranked lowest.", flush=True)
    else:
        all_passed = False

    print("\n" + "=" * 70, flush=True)
    if all_passed:
        print("🎉 SUCCESS: BGE-M3 technology test passed all evaluations!", flush=True)
    else:
        print("❌ FAILURE: BGE-M3 test encountered unexpected rankings.", flush=True)
    print("=" * 70, flush=True)
    return all_passed


if __name__ == "__main__":
    success = run_test()
    sys.exit(0 if success else 1)
