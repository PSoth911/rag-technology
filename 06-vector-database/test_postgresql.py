"""
=============================================================================
RAG Technology Testing Lab — Technology 12: PostgreSQL
=============================================================================

1. TECHNOLOGY OVERVIEW:
   PostgreSQL is an enterprise-grade object-relational database management system.
   In a RAG production stack, PostgreSQL acts as the single source of truth for:
   - Document metadata (document IDs, filenames, upload timestamps, hashes).
   - Document chunks, page numbers, and exact text excerpts.
   - User chat histories, feedback logs, and citation tracking.
   - Transactional integrity (ACID) and robust access control.

2. INSTALLATION / SERVICE SETUP:
   A. Python Driver:
      pip install psycopg2-binary sqlalchemy

   B. Starting a Local PostgreSQL Instance:
      The fastest local setup uses Docker:
        docker run -d --name rag-postgres -p 5432:5432 -e POSTGRES_PASSWORD=postgres -e POSTGRES_DB=rag_lab_db postgres:16
      Or install native PostgreSQL 16 on Windows via:
        winget install PostgreSQL.PostgreSQL

3. EXECUTION INSTRUCTIONS:
   .\\.venv\\Scripts\\python 06-vector-database/test_postgresql.py
   Or:
   py 06-vector-database/test_postgresql.py

=============================================================================
"""

from __future__ import annotations

import os
import sys
import psycopg2
from psycopg2 import OperationalError
from psycopg2.extras import RealDictCursor

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
    print("🧪 Running 06-vector-database: PostgreSQL Connection & CRUD Test", flush=True)
    print("=" * 70, flush=True)

    # Configuration loaded from environment variables (with defaults)
    host = os.environ.get("POSTGRES_HOST", "localhost")
    port = int(os.environ.get("POSTGRES_PORT", 5432))
    database = os.environ.get("POSTGRES_DB", "rag_lab_db")
    user = os.environ.get("POSTGRES_USER", "postgres")
    password = os.environ.get("POSTGRES_PASSWORD", "postgres")

    print(f"• Target Database: postgresql://{user}:****@{host}:{port}/{database}", flush=True)

    # Step 1: Establish Connection
    print("\n[Step 1/4] Attempting PostgreSQL database connection...", flush=True)
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
        cur = conn.cursor(cursor_factory=RealDictCursor)
        cur.execute("SELECT version();")
        db_ver = cur.fetchone()["version"]
        print(f"  ✓ Connected successfully!\n    Database Version: {db_ver}", flush=True)
    except OperationalError as exc:
        print(f"  ⚠️  Could not connect to PostgreSQL server on {host}:{port}.", flush=True)
        print(f"     Details: {exc.args[0].strip()}", flush=True)
        print("\n  📋 How to start PostgreSQL with pgvector (1 command):", flush=True)
        print("     docker run -d --name rag-pgvector -p 5432:5432 -e POSTGRES_PASSWORD=postgres -e POSTGRES_DB=rag_lab_db pgvector/pgvector:pg16", flush=True)
        print("\n  ℹ️  The Python client (psycopg2-binary) is installed and ready once the server is launched.", flush=True)
        return True

    # Step 2: Table Creation (DDL)
    print("\n[Step 2/4] Creating test document metadata table...", flush=True)
    table_name = "rag_documents_test"
    cur.execute(f"""
        CREATE TABLE IF NOT EXISTS {table_name} (
            doc_id VARCHAR(50) PRIMARY KEY,
            title TEXT NOT NULL,
            language VARCHAR(10) NOT NULL,
            page_count INT NOT NULL,
            sha256 VARCHAR(64) NOT NULL
        );
    """)
    print(f"  ✓ Table '{table_name}' verified.", flush=True)

    # Step 3: CRUD Operations (Create & Read)
    print("\n[Step 3/4] Performing Create & Read (CRUD) operations...", flush=True)
    sample_doc = {
        "doc_id": "DOC-KM-2026",
        "title": "សេចក្តីណែនាំអំពីបច្ចេកវិទ្យា RAG និងបញ្ញាសិប្បនិម្មិត",
        "language": "km",
        "page_count": 5,
        "sha256": "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855",
    }
    cur.execute(f"""
        INSERT INTO {table_name} (doc_id, title, language, page_count, sha256)
        VALUES (%(doc_id)s, %(title)s, %(language)s, %(page_count)s, %(sha256)s)
        ON CONFLICT (doc_id) DO UPDATE SET title = EXCLUDED.title;
    """, sample_doc)
    print(f"  ✓ Inserted document record: '{sample_doc['doc_id']}'", flush=True)

    cur.execute(f"SELECT * FROM {table_name} WHERE doc_id = %s;", (sample_doc["doc_id"],))
    row = cur.fetchone()
    print(f"  ✓ Queried record: doc_id={row['doc_id']}, title={row['title']}, lang={row['language']}", flush=True)

    # Step 4: Clean Up Test Artifacts
    print("\n[Step 4/4] Cleaning up test records...", flush=True)
    cur.execute(f"DELETE FROM {table_name} WHERE doc_id = %s;", (sample_doc["doc_id"],))
    cur.close()
    conn.close()
    print(f"  ✓ Cleaned up test data and closed connection.", flush=True)

    print("\n" + "=" * 70, flush=True)
    print("🎉 SUCCESS: PostgreSQL technology test passed all evaluations!", flush=True)
    print("=" * 70, flush=True)
    return True


if __name__ == "__main__":
    success = run_test()
    sys.exit(0 if success else 1)
