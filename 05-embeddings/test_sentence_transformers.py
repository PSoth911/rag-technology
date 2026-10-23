"""
=============================================================================
RAG Technology Testing Lab — Technology 11: Sentence Transformers
=============================================================================

1. TECHNOLOGY OVERVIEW:
   Sentence Transformers is the standard Python framework for computing dense
   vector embeddings of sentences, paragraphs, and images.
   In a RAG system, Sentence Transformers:
   - Loads pretrained transformer checkpoints locally (PyTorch/ONNX).
   - Encodes text chunks into fixed-dimensional semantic vector spaces.
   - Computes cosine similarity matrices for ranking candidate passages.

2. INSTALLATION / PREREQUISITES:
   pip install sentence-transformers torch numpy

3. EXECUTION INSTRUCTIONS:
   .\\.venv\\Scripts\\python 05-embeddings/test_sentence_transformers.py
   Or:
   py 05-embeddings/test_sentence_transformers.py

=============================================================================
"""

from __future__ import annotations

import sys
import time
from pathlib import Path
import numpy as np

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
    print("=" * 70)
    print("🧪 Running 05-embeddings: Sentence Transformers Baseline Test")
    print("=" * 70)

    try:
        from sentence_transformers import SentenceTransformer, util
        import sentence_transformers
        print(f"• Sentence Transformers Version: {sentence_transformers.__version__}")
    except ImportError as exc:
        print(f"❌ Failed to import sentence_transformers: {exc}")
        return False

    all_passed = True
    model_name = "paraphrase-MiniLM-L3-v2"  # Fast, lightweight (61 MB) for validation

    # Step 1: Load SentenceTransformer model
    print(f"\n[Step 1/4] Loading model checkpoint: '{model_name}'...")
    start_load = time.perf_counter()
    try:
        model = SentenceTransformer(model_name)
        load_time = round(time.perf_counter() - start_load, 2)
        dim = model.get_sentence_embedding_dimension()
        print(f"  ✓ Model loaded in {load_time}s. Embedding dimension: {dim}")
    except Exception as exc:
        print(f"  ✗ Model load failed: {exc}")
        return False

    # Step 2: Encode sentences into dense vectors
    print("\n[Step 2/4] Encoding sample passages into embeddings...")
    sentences = [
        "Retrieval-Augmented Generation enhances LLMs with external documents.",
        "PostgreSQL pgvector stores high-dimensional embeddings for similarity search.",
        "Pizza with extra cheese and tomato sauce baked in an oven.",
    ]
    query = "How do we store vector embeddings in databases?"

    start_enc = time.perf_counter()
    embeddings = model.encode(sentences, convert_to_tensor=True)
    query_embedding = model.encode(query, convert_to_tensor=True)
    enc_time = round((time.perf_counter() - start_enc) * 1000, 2)

    print(f"  ✓ Encoded 3 passages + 1 query in {enc_time}ms.")
    print(f"  ✓ Passage embeddings shape: {embeddings.shape}")
    print(f"  ✓ Query embedding shape   : {query_embedding.shape}")

    # Step 3: Compute Cosine Similarity Matrix
    print("\n[Step 3/4] Computing Cosine Similarities against query:")
    print(f"  Query: \"{query}\"")
    cosine_scores = util.cos_sim(query_embedding, embeddings)[0]

    ranked_results = []
    for i in range(len(sentences)):
        score = float(cosine_scores[i])
        ranked_results.append((score, sentences[i]))

    # Sort descending
    ranked_results.sort(key=lambda x: x[0], reverse=True)

    for rank, (score, passage) in enumerate(ranked_results, 1):
        print(f"  Rank {rank} (score={score:.4f}): \"{passage}\"")

    # Step 4: Validate Semantic Retrieval Logic
    print("\n[Step 4/4] Validating ranking correctness...")
    # The database sentence should be ranked highest for a database query
    top_hit_text = ranked_results[0][1]
    bottom_hit_text = ranked_results[-1][1]

    if "PostgreSQL" in top_hit_text:
        print("  ✓ Correct: Most relevant database passage ranked #1.")
    else:
        print(f"  ✗ Warning: Unexpected top hit: {top_hit_text}")
        all_passed = False

    if "Pizza" in bottom_hit_text:
        print("  ✓ Correct: Irrelevant distractor ranked lowest.")
    else:
        print(f"  ✗ Warning: Distractor was not lowest ranked.")
        all_passed = False

    print("\n" + "=" * 70)
    if all_passed:
        print("🎉 SUCCESS: Sentence Transformers technology test passed all evaluations!")
    else:
        print("❌ FAILURE: Sentence Transformers test failed evaluation.")
    print("=" * 70)
    return all_passed


if __name__ == "__main__":
    success = run_test()
    sys.exit(0 if success else 1)
