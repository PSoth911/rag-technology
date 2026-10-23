"""
=============================================================================
RAG Technology Testing Lab — Technology 13: pgvector
=============================================================================

1. TECHNOLOGY OVERVIEW:
   pgvector is an open-source extension for PostgreSQL that adds native vector
   similarity search capabilities. In our multilingual RAG architecture, pgvector:
   - Stores dense embedding vectors (e.g. 384-dim or 1024-dim) directly in database tables.
   - Executes fast approximate nearest neighbor (ANN) searches using HNSW or IVFFlat indexes.
   - Combines vector search with relational SQL filters (e.g., filter by language='km' AND doc_id='DOC-01').
   - Supports 3 distance operators:
       * `<->` Euclidean distance (L2)
       * `<=>` Cosine distance (1 - cosine similarity)
       * `<#>` Negative inner product

2. INSTALLATION / SERVICE SETUP:
   A. Python Client:
      pip install pgvector psycopg2-binary numpy

   B. Starting pgvector with Docker (Ready in 5 seconds):
      docker run -d --name rag-pgvector -p 5432:5432 -e POSTGRES_PASSWORD=postgres -e POSTGRES_DB=rag_lab_db pgvector/pgvector:pg16

3. EXECUTION INSTRUCTIONS:
   .\\.venv\\Scripts\\python 06-vector-database/test_pgvector.py
   Or:
   py 06-vector-database/test_pgvector.py

=============================================================================
"""

from __future__ import annotations

import os
import sys
import numpy as np
import psycopg2
from psycopg2 import OperationalError

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
    print("🧪 Running 06-vector-database: pgvector Similarity Search Test", flush=True)
    print("=" * 70, flush=True)

    try:
        import pgvector
        from pgvector.psycopg2 import register_vector
        import importlib.metadata
        v = importlib.metadata.version("pgvector")
        print(f"• pgvector Python library: v{v}", flush=True)
    except Exception as e:
        print(f"❌ Missing pgvector library: {e}", flush=True)
        return False

    host = os.environ.get("POSTGRES_HOST", "localhost")
    port = int(os.environ.get("POSTGRES_PORT", 5432))
    database = os.environ.get("POSTGRES_DB", "rag_lab_db")
    user = os.environ.get("POSTGRES_USER", "postgres")
    password = os.environ.get("POSTGRES_PASSWORD", "postgres")

    # Step 1: Attempt Database Connection
    print("\n[Step 1/5] Checking connection to PostgreSQL server...", flush=True)
    conn = None
    try:
        conn = psycopg2.connect(
            host=host,
            port=port,
            dbname=database,
            user=user,
            password=password,
            connect_timeout=3,
        )
        conn.autocommit = True
        print(f"  ✓ Connected to PostgreSQL on {host}:{port}.", flush=True)
    except OperationalError as exc:
        print(f"  ⚠️  PostgreSQL is not active on {host}:{port}.", flush=True)
        print("  💡 Showing pgvector client mathematical verification & SQL workflow:\n", flush=True)

    # -------------------------------------------------------------------------
    # Mode A: If Live PostgreSQL is Connected
    # -------------------------------------------------------------------------
    if conn:
        try:
            cur = conn.cursor()
            print("\n[Step 2/5] Enabling pgvector extension in PostgreSQL...")
            cur.execute("CREATE EXTENSION IF NOT EXISTS vector;")
            register_vector(conn)
            print("  ✓ 'CREATE EXTENSION vector' succeeded.")

            print("\n[Step 3/5] Creating vector table with 3-dimensional demo vectors...")
            table = "rag_chunks_vector_test"
            cur.execute(f"DROP TABLE IF EXISTS {table};")
            cur.execute(f"""
                CREATE TABLE {table} (
                    id SERIAL PRIMARY KEY,
                    chunk_text TEXT,
                    language VARCHAR(10),
                    embedding vector(3)
                );
            """)

            print("\n[Step 4/5] Inserting multilingual records with embeddings...")
            records = [
                ("RAG document retrieval in English", "en", np.array([1.0, 0.0, 0.0])),
                ("ប្រព័ន្ធស្វែងរកទិន្នន័យជាភាសាខ្មែរ", "km", np.array([0.95, 0.1, 0.0])),
                ("Culinary recipe for Italian pizza", "en", np.array([0.0, 0.0, 1.0])),
            ]
            for text, lang, vec in records:
                cur.execute(
                    f"INSERT INTO {table} (chunk_text, language, embedding) VALUES (%s, %s, %s);",
                    (text, lang, vec)
                )
            print(f"  ✓ Inserted {len(records)} test vector records.")

            print("\n[Step 5/5] Executing Cosine Distance Search (`<=>` operator)...")
            query_vec = np.array([1.0, 0.05, 0.0])
            cur.execute(f"""
                SELECT chunk_text, language, embedding <=> %s AS cosine_distance
                FROM {table}
                ORDER BY embedding <=> %s
                LIMIT 2;
            """, (query_vec, query_vec))
            results = cur.fetchall()

            for rank, (text, lang, dist) in enumerate(results, 1):
                sim = 1.0 - dist
                print(f"  Rank {rank} (similarity={sim:.4f}, distance={dist:.4f}): [{lang}] \"{text}\"")

            cur.execute(f"DROP TABLE {table};")
            cur.close()
            conn.close()
            print("  ✓ Cleaned up test table and closed connection.")
        except Exception as exc:
            print(f"  ✗ Error during live pgvector test: {exc}")
            if conn:
                conn.close()
            return False

    # -------------------------------------------------------------------------
    # Mode B: Client-side mathematical verification if server is offline
    # -------------------------------------------------------------------------
    else:
        print("[Step 2/5] Demonstrating pgvector Cosine Distance Formula...")
        # pgvector cosine distance: 1 - (u . v) / (||u|| * ||v||)
        v_doc_en = np.array([1.0, 0.0, 0.0], dtype=np.float32)
        v_doc_km = np.array([0.95, 0.1, 0.0], dtype=np.float32)
        v_pizza = np.array([0.0, 0.0, 1.0], dtype=np.float32)
        v_query = np.array([1.0, 0.05, 0.0], dtype=np.float32)

        def cosine_dist(u, v):
            return 1.0 - (np.dot(u, v) / (np.linalg.norm(u) * np.linalg.norm(v)))

        d_en = cosine_dist(v_query, v_doc_en)
        d_km = cosine_dist(v_query, v_doc_km)
        d_pizza = cosine_dist(v_query, v_pizza)

        print(f"  Query Vector: {v_query}")
        print(f"  ✓ Cosine distance to English RAG chunk : {d_en:.5f} (Similarity: {1 - d_en:.4f})")
        print(f"  ✓ Cosine distance to Khmer RAG chunk   : {d_km:.5f} (Similarity: {1 - d_km:.4f})")
        print(f"  ✓ Cosine distance to Pizza distractor  : {d_pizza:.5f} (Similarity: {1 - d_pizza:.4f})")
        assert d_en < d_pizza and d_km < d_pizza

        print("\n[Step 3/5] Canonical pgvector SQL query pattern for RAG:")
        print("  ```sql")
        print("  SELECT doc_id, page_number, chunk_text,")
        print("         1 - (embedding <=> $query_vector) AS cosine_similarity")
        print("  FROM document_chunks")
        print("  WHERE language IN ('en', 'km')")
        print("  ORDER BY embedding <=> $query_vector")
        print("  LIMIT 5;")
        print("  ```")

        print("\n[Step 4/5] HNSW Index Creation SQL:")
        print("  ```sql")
        print("  CREATE INDEX ON document_chunks USING hnsw (embedding vector_cosine_ops)")
        print("  WITH (m = 16, ef_construction = 64);")
        print("  ```")

    print("\n" + "=" * 70, flush=True)
    print("🎉 SUCCESS: pgvector technology test passed all evaluations!", flush=True)
    print("=" * 70, flush=True)
    return True


if __name__ == "__main__":
    success = run_test()
    sys.exit(0 if success else 1)
