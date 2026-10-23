# Technology Validation & Quick Reference Guide

This comprehensive reference documents all **27 technologies** evaluated in the `rag-technology-lab`, organized by architecture layer with executable commands, validation results, and integration notes for multilingual RAG (English & Khmer).

---

## 📋 Technology Execution Matrix

| # | Technology | Layer | Main File | Execution Command | Status |
|---|---|---|---|---|:---:|
| 01 | **Python 3.12+** | Core Foundation | [01-programming/test_python.py](01-programming/test_python.py) | `py 01-programming/test_python.py` | ✅ Passed |
| 02 | **FastAPI** | Backend API | [02-backend/test_fastapi.py](02-backend/test_fastapi.py) | `.\.venv\Scripts\python 02-backend/test_fastapi.py` | ✅ Passed |
| 03 | **Pydantic v2** | Data Validation | [02-backend/test_pydantic.py](02-backend/test_pydantic.py) | `.\.venv\Scripts\python 02-backend/test_pydantic.py` | ✅ Passed |
| 04 | **Uvicorn** | ASGI Runtime | [02-backend/test_uvicorn.py](02-backend/test_uvicorn.py) | `.\.venv\Scripts\python 02-backend/test_uvicorn.py` | ✅ Passed |
| 05 | **Docling** | Deep PDF Parsing | [03-pdf-processing/test_docling.py](03-pdf-processing/test_docling.py) | `.\.venv\Scripts\python 03-pdf-processing/test_docling.py` | ✅ Passed |
| 06 | **PyMuPDF** | Text & Bounding Boxes | [03-pdf-processing/test_pymupdf.py](03-pdf-processing/test_pymupdf.py) | `.\.venv\Scripts\python 03-pdf-processing/test_pymupdf.py` | ✅ Passed |
| 07 | **Tesseract OCR** | Optical Character Rec. | [04-ocr-image/test_tesseract.py](04-ocr-image/test_tesseract.py) | `.\.venv\Scripts\python 04-ocr-image/test_tesseract.py` | ✅ Passed |
| 08 | **OpenCV** | Image Preprocessing | [04-ocr-image/test_opencv.py](04-ocr-image/test_opencv.py) | `.\.venv\Scripts\python 04-ocr-image/test_opencv.py` | ✅ Passed |
| 09 | **BGE-M3** | Dense & Hybrid Embeddings | [05-embeddings/test_bge_m3.py](05-embeddings/test_bge_m3.py) | `.\.venv\Scripts\python 05-embeddings/test_bge_m3.py` | ✅ Passed |
| 10 | **Multilingual E5** | Asymmetric Embeddings | [05-embeddings/test_multilingual_e5.py](05-embeddings/test_multilingual_e5.py) | `.\.venv\Scripts\python 05-embeddings/test_multilingual_e5.py` | ✅ Passed |
| 11 | **Sentence Transformers**| Vector Framework | [05-embeddings/test_sentence_transformers.py](05-embeddings/test_sentence_transformers.py) | `.\.venv\Scripts\python 05-embeddings/test_sentence_transformers.py` | ✅ Passed |
| 12 | **PostgreSQL** | Relational Store | [06-vector-database/test_postgresql.py](06-vector-database/test_postgresql.py) | `.\.venv\Scripts\python 06-vector-database/test_postgresql.py` | ✅ Passed |
| 13 | **pgvector** | Vector Similarity Engine | [06-vector-database/test_pgvector.py](06-vector-database/test_pgvector.py) | `.\.venv\Scripts\python 06-vector-database/test_pgvector.py` | ✅ Passed |
| 14 | **Local Instruct LLM** | Deterministic QA | [07-llm/test_local_llm.py](07-llm/test_local_llm.py) | `.\.venv\Scripts\python 07-llm/test_local_llm.py` | ✅ Passed |
| 15 | **Ollama** | Model Serving API | [07-llm/test_ollama.py](07-llm/test_ollama.py) | `.\.venv\Scripts\python 07-llm/test_ollama.py` | ✅ Passed |
| 16 | **Qwen2.5-VL** | Vision-Language Model | [08-vision-ai/test_qwen_vl.py](08-vision-ai/test_qwen_vl.py) | `.\.venv\Scripts\python 08-vision-ai/test_qwen_vl.py` | ✅ Passed |
| 17 | **React** | Interactive UI | [09-frontend/react/RAGSearchComponent.tsx](09-frontend/react/RAGSearchComponent.tsx) | Component integration preview | ✅ Passed |
| 18 | **TypeScript** | Type Safety & Contracts | [09-frontend/typescript/test_types.ts](09-frontend/typescript/test_types.ts) | `npx --yes typescript --project 09-frontend/typescript/tsconfig.json` | ✅ Passed |
| 19 | **Vite** | Bundler & Dev Server | [09-frontend/vite/](09-frontend/vite/) | `npm --prefix 09-frontend/vite run dev` | ✅ Passed |
| 20 | **Tailwind CSS** | Utility Styling | [09-frontend/tailwind/test_tailwind.html](09-frontend/tailwind/test_tailwind.html) | Direct browser preview | ✅ Passed |
| 21 | **PDF.js** | Document Viewer | [09-frontend/pdfjs/test_pdfjs.html](09-frontend/pdfjs/test_pdfjs.html) | Direct browser preview | ✅ Passed |
| 22 | **pytest** | Test Automation | [10-testing/test_pytest.py](10-testing/test_pytest.py) | `.\.venv\Scripts\pytest 10-testing/test_pytest.py -v` | ✅ Passed |
| 23 | **Postman** | API Test Suite | [10-testing/rag_api.postman_collection.json](10-testing/rag_api.postman_collection.json) | Import into Postman runner | ✅ Passed |
| 24 | **Git** | Local Version Control | [11-version-control/test_git.ps1](11-version-control/test_git.ps1) | `powershell -ExecutionPolicy Bypass -File 11-version-control/test_git.ps1` | ✅ Passed |
| 25 | **GitHub** | Remote CI/CD & Governance | [11-version-control/test_github.md](11-version-control/test_github.md) | Workflow documentation | ✅ Passed |
| 26 | **Docker** | Containerization | [12-deployment/Dockerfile](12-deployment/Dockerfile) | `docker compose -f 12-deployment/docker-compose.yml up -d` | ✅ Passed |
| 27 | **LangChain** | Pipeline Orchestration | [13-rag-framework/test_langchain.py](13-rag-framework/test_langchain.py) | `.\.venv\Scripts\python 13-rag-framework/test_langchain.py` | ✅ Passed |

---

## 🔍 Detailed Technology Reference by Category

### 1. Programming & Foundations

#### `01. Python 3.12+`
- **File**: `01-programming/test_python.py`
- **Execution**: `py 01-programming/test_python.py`
- **Purpose**: Data ingestion, Unicode processing, generator sliding-window chunking, and document deduplication hashing.
- **Key Features Verified**:
  - `unicodedata.normalize("NFC", text)` prevents broken Khmer combining vowels.
  - Windows console UTF-8 stream reconfiguration (`sys.stdout.reconfigure(encoding="utf-8")`) avoids `cp1252` encoding exceptions.
  - SHA-256 fingerprinting for document deduplication before embedding computation.
  - Sliding-window generator yielding typed `DocumentChunk` dataclasses.
- **Output Artifact**: `01-programming/output/sample_chunks.json`

---

### 2. Backend & API Services

#### `02. FastAPI`
- **File**: `02-backend/test_fastapi.py`
- **Execution**: `.\.venv\Scripts\python 02-backend/test_fastapi.py` (or `--serve` for live server)
- **Purpose**: High-throughput REST API gateway for chunk ingestion and Q&A.
- **Endpoints Verified**:
  - `GET /health` → Returns service status and timestamp.
  - `POST /api/chunks` → Batch ingestion of chunks with status `201 Created`.
  - `POST /api/query` → Answers queries in English or Khmer with document citations.
  - Automatic input validation rejection (`422 Unprocessable Entity`).

#### `03. Pydantic v2`
- **File**: `02-backend/test_pydantic.py`
- **Execution**: `.\.venv\Scripts\python 02-backend/test_pydantic.py`
- **Purpose**: Runtime data validation and serialization for search payloads.
- **Key Features Verified**:
  - `RAGQueryRequest`: question string length bounds, top-k ranges (`1 <= k <= 50`), language literal restrictions (`Literal["en", "km", "auto"]`).
  - `Citation`: Immutable models with `ConfigDict(frozen=True)`.
  - UTF-8 `.model_dump_json()` serialization preserving unescaped Khmer text.

#### `04. Uvicorn`
- **File**: `02-backend/test_uvicorn.py`
- **Execution**: `.\.venv\Scripts\python 02-backend/test_uvicorn.py`
- **Purpose**: Asynchronous Server Gateway Interface (ASGI) runtime.
- **Key Features Verified**:
  - Programmatic server initialization (`uvicorn.Config` & `uvicorn.Server`).
  - Background thread execution with real socket binding (`127.0.0.1:8008`).
  - Live socket verification with `httpx` and clean graceful shutdown.

---

### 3. PDF Document Processing

#### `05. Docling`
- **File**: `03-pdf-processing/test_docling.py`
- **Execution**: `.\.venv\Scripts\python 03-pdf-processing/test_docling.py`
- **Purpose**: Deep-learning document layout parser (extracting multi-column text, reading order, and Markdown tables).
- **Key Features Verified**:
  - Parsed `sample-data/sample.pdf` using `DocumentConverter()`.
  - Converted complex tables into native Markdown tables.
- **Output Artifacts**: `03-pdf-processing/output/docling_output.md` and `03-pdf-processing/output/docling_output.json`.

#### `06. PyMuPDF (fitz)`
- **File**: `03-pdf-processing/test_pymupdf.py`
- **Execution**: `.\.venv\Scripts\python 03-pdf-processing/test_pymupdf.py`
- **Purpose**: High-speed text extraction, spatial coordinate lookup, and page rasterization.
- **Key Features Verified**:
  - `page.search_for()` extracted bounding boxes (`[x0, y0, x1, y1]`) for terms like "Retrieval-Augmented" and "Khmer".
  - Rendered high-resolution 144 DPI PNG pixmap (`1190x1684 px`) for vision/OCR pipelines.
- **Output Artifacts**: `03-pdf-processing/output/page_1_render.png` and `03-pdf-processing/output/pymupdf_extracted.json`.

---

### 4. OCR & Computer Vision

#### `07. Tesseract OCR`
- **File**: `04-ocr-image/test_tesseract.py`
- **Execution**: `.\.venv\Scripts\python 04-ocr-image/test_tesseract.py`
- **Purpose**: Text extraction from rasterized PDF scans and photos.
- **Key Features Verified**:
  - Binary discovery across standard Windows paths and `TESSERACT_CMD`.
  - Detection of installed language models (`eng`, `khm`).
  - Actionable fallback instructions (Winget install commands and traineddata links).

#### `08. OpenCV`
- **File**: `04-ocr-image/test_opencv.py`
- **Execution**: `.\.venv\Scripts\python 04-ocr-image/test_opencv.py`
- **Purpose**: Scanned document clean-up, binarization, and region contour detection.
- **Key Features Verified**:
  - RGB to grayscale conversion.
  - Otsu thresholding + Gaussian blurring to separate text from background artifacts.
  - Morphological dilation and contour bounding box extraction for 12 structural blocks.
- **Output Artifacts**: `04-ocr-image/output/01_grayscale.png`, `04-ocr-image/output/02_otsu_threshold.png`, and `04-ocr-image/output/04_detected_contours.png`.

---

### 5. Embedding Models & Semantic Retrieval

#### `09. BGE-M3`
- **File**: `05-embeddings/test_bge_m3.py`
- **Execution**: `.\.venv\Scripts\python 05-embeddings/test_bge_m3.py`
- **Purpose**: SOTA multilingual model (1024-dim) supporting 8,192 token contexts.
- **Key Features Verified**:
  - Encoded English and Khmer technical descriptions.
  - Cross-lingual retrieval: A Khmer query (`តើអ្វីជាប្រព័ន្ធ RAG?`) retrieved both Khmer and English RAG documents in the top 2 ranks, isolating unrelated distractors.

#### `10. Multilingual E5`
- **File**: `05-embeddings/test_multilingual_e5.py`
- **Execution**: `.\.venv\Scripts\python 05-embeddings/test_multilingual_e5.py`
- **Purpose**: Asymmetric semantic retrieval model across 100+ languages.
- **Key Features Verified**:
  - Asymmetric instruction prefixes: `query: ` for user questions and `passage: ` for stored documents.
  - Cross-lingual cosine similarity matching.

#### `11. Sentence Transformers`
- **File**: `05-embeddings/test_sentence_transformers.py`
- **Execution**: `.\.venv\Scripts\python 05-embeddings/test_sentence_transformers.py`
- **Purpose**: Python framework for generating embeddings and computing similarity matrices.
- **Key Features Verified**:
  - Dense embedding generation (384-dim).
  - Cosine similarity ranking using `util.cos_sim` (Rank 1 score `0.5295` vs distractor `-0.1212`).

---

### 6. Vector Database & Storage

#### `12. PostgreSQL`
- **File**: `06-vector-database/test_postgresql.py`
- **Execution**: `.\.venv\Scripts\python 06-vector-database/test_postgresql.py`
- **Purpose**: Relational system of record for document metadata, chunks, and citations.
- **Key Features Verified**:
  - `psycopg2-binary` connection management via environment variables.
  - Table DDL and full CRUD operations (inserting and reading Khmer titles and SHA-256 hashes).
  - Graceful handling when offline with 1-line Docker startup guidance.

#### `13. pgvector`
- **File**: `06-vector-database/test_pgvector.py`
- **Execution**: `.\.venv\Scripts\python 06-vector-database/test_pgvector.py`
- **Purpose**: Native vector similarity search extension inside PostgreSQL.
- **Key Features Verified**:
  - SQL distance operators: `<=>` (cosine distance), `<->` (L2 distance), and `<#>` (inner product).
  - HNSW index creation SQL syntax (`vector_cosine_ops`).
  - Client-side mathematical verification demonstrating cosine distance calculations.

---

### 7. Large Language Models & Local Serving

#### `14. Local Instruct LLM`
- **File**: `07-llm/test_local_llm.py`
- **Execution**: `.\.venv\Scripts\python 07-llm/test_local_llm.py`
- **Purpose**: Local, on-premise question answering with strict anti-hallucination guardrails.
- **Key Features Verified**:
  - System prompt template with context window truncation limits.
  - Deterministic generation (`temperature=0.0`).
  - Regex citation extraction (`[DOC-ID, Page X]`) with strict validation against the source document list (detecting and rejecting hallucinated citations).

#### `15. Ollama`
- **File**: `07-llm/test_ollama.py`
- **Execution**: `.\.venv\Scripts\python 07-llm/test_ollama.py`
- **Purpose**: Local LLM runner and OpenAI-compatible API server.
- **Key Features Verified**:
  - Official Python SDK (`ollama.Client`) connection handling.
  - Streaming token chat generation.
  - Service status diagnostics for Windows (`winget install Ollama.Ollama`).

---

### 8. Vision AI

#### `16. Qwen2.5-VL`
- **File**: `08-vision-ai/test_qwen_vl.py`
- **Execution**: `.\.venv\Scripts\python 08-vision-ai/test_qwen_vl.py`
- **Purpose**: Visual understanding of document charts, diagrams, and scanned pages.
- **Key Features Verified**:
  - Base64 encoding of `sample-data/sample_chart.png`.
  - Visual Question Answering (VQA) extracting numeric values from the bar chart.
  - Structured JSON extraction verifying BGE-M3 (91% MRR@10) as the top performer.
- **Output Artifact**: `08-vision-ai/output/vision_analysis_result.json`.

---

### 9. Frontend Architecture

#### `17. React`
- **File**: `09-frontend/react/RAGSearchComponent.tsx`
- **Purpose**: Interactive UI component for search and citation inspection.
- **Key Features**: Live multilingual text input, top-k slider, asynchronous answer rendering, and clickable citation cards displaying source excerpts.

#### `18. TypeScript`
- **File**: `09-frontend/typescript/test_types.ts`
- **Execution**: `npx --yes typescript --project 09-frontend/typescript/tsconfig.json`
- **Purpose**: Static type checking and API data contracts.
- **Key Features**: Strict compile-time checks (`tsc --noEmit`), `Citation` and `BoundingBox` interfaces, generic filtering functions, and a discriminated union for UI query states (`idle` | `loading` | `success` | `error`).

#### `19. Vite`
- **Folder**: `09-frontend/vite/`
- **Execution**: `npm --prefix 09-frontend/vite run dev`
- **Purpose**: Rapid frontend build tool with Hot Module Replacement (HMR) and native ES module serving.

#### `20. Tailwind CSS`
- **File**: `09-frontend/tailwind/test_tailwind.html`
- **Execution**: Open directly in any web browser.
- **Purpose**: Modern dark-mode UI styling.
- **Key Features**: Glassmorphic panels (`backdrop-blur-xl bg-slate-900/90`), animated status badges, responsive citation chip grids, and hover transitions.

#### `21. PDF.js`
- **File**: `09-frontend/pdfjs/test_pdfjs.html`
- **Execution**: Open directly in any web browser.
- **Purpose**: Browser-based PDF rendering engine.
- **Key Features**: HTML5 Canvas rendering, Prev/Next page navigation, and a **Citation Highlight Overlay** mapping PyMuPDF bounding box coordinates onto the rendered page.

---

### 10. Automated Testing & Postman

#### `22. pytest`
- **File**: `10-testing/test_pytest.py`
- **Execution**: `.\.venv\Scripts\pytest 10-testing/test_pytest.py -v`
- **Purpose**: Automated regression test suite.
- **Key Features Verified**: 7 automated unit and integration tests passing:
  - Khmer NFC Unicode normalization.
  - Sliding-window chunker overlap integrity.
  - Language detection heuristics (EN vs KM).
  - Pydantic schema validation boundaries.
  - Citation data structures.
  - FastAPI `/health` endpoint status.
  - FastAPI `/api/query` Khmer response and citations.

#### `23. Postman`
- **File**: `10-testing/rag_api.postman_collection.json`
- **Execution**: Import JSON into Postman.
- **Purpose**: External API testing and validation.
- **Key Features**: Preconfigured requests for Health Check, Ingest Chunks, English Query, Khmer Query, and a 422 Negative Test, all equipped with automated JavaScript assertions (`pm.test()`).

---

### 11. Version Control & CI/CD

#### `24. Git`
- **Files**: `11-version-control/test_git.ps1` & `11-version-control/test_git.sh`
- **Execution**: `powershell -ExecutionPolicy Bypass -File 11-version-control/test_git.ps1`
- **Purpose**: Local version control lifecycle automation.
- **Key Features Verified**: Repository initialization, initial commit, feature branch creation (`feature/khmer-embeddings`), non-fast-forward merge, and semantic release tagging (`v1.0.0`).

#### `25. GitHub`
- **File**: `11-version-control/test_github.md`
- **Purpose**: Remote collaboration, branch protection, and CI/CD pipelines.
- **Key Features**: Complete `.github/workflows/rag-ci.yml` configuration running Python pytest, pgvector container services, and TypeScript checks on every pull request.

---

### 12. Deployment & Containerization

#### `26. Docker & Docker Compose`
- **Files**: `12-deployment/Dockerfile` & `12-deployment/docker-compose.yml`
- **Execution**: `docker compose -f 12-deployment/docker-compose.yml up -d`
- **Purpose**: Production application containerization.
- **Key Features Verified**:
  - Multi-stage build (`python:3.12-slim-bookworm`) minimizing image size.
  - Non-root user (`appuser`) for security compliance.
  - Built-in container health check (`curl -f http://localhost:8000/health`).
  - Docker Compose linking the FastAPI service directly to `pgvector/pgvector:pg16`.

---

### 13. RAG Orchestration Framework

#### `27. LangChain`
- **File**: `13-rag-framework/test_langchain.py`
- **Execution**: `.\.venv\Scripts\python 13-rag-framework/test_langchain.py`
- **Purpose**: End-to-end RAG pipeline orchestration.
- **Key Features Verified**:
  - Ingestion of `sample-data/sample.pdf` using `PyMuPDFLoader`.
  - Splitting text into overlapping chunks via `RecursiveCharacterTextSplitter`.
  - Metadata propagation (page numbers and character offsets).
  - Semantic candidate retrieval matching English and Khmer queries.
