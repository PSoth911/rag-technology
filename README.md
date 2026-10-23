# RAG Technology Lab (`rag-technology-lab`)

A systematic, modular testing laboratory to evaluate and validate every underlying technology for an advanced multilingual RAG system (supporting PDF ingestion, English and Khmer text, semantic retrieval, citations, and visual document understanding).

---

## 🗂 Project Structure

```text
rag-technology-lab/
├── 01-programming/               # Python 3.12+ fundamentals & data structures for RAG
├── 02-backend/                   # FastAPI, Pydantic, Uvicorn API testing
├── 03-pdf-processing/            # Docling & PyMuPDF document extraction
├── 04-ocr-image/                 # Tesseract OCR (Khmer & English) & OpenCV preprocessing
├── 05-embeddings/                # BGE-M3, Multilingual E5, Sentence Transformers
├── 06-vector-database/           # PostgreSQL & pgvector similarity search
├── 07-llm/                       # Local instruct models & Ollama integration
├── 08-vision-ai/                 # Qwen2.5-VL for charts, tables & visual QA
├── 09-frontend/                  # React, TypeScript, Vite, Tailwind CSS, PDF.js
├── 10-testing/                   # Pytest automation & Postman API collections
├── 11-version-control/           # Git automation & GitHub workflow notes
├── 12-deployment/                # Docker containerization & multi-stage builds
├── 13-rag-framework/             # LangChain document loaders, chunking & retrieval
└── sample-data/                  # Multilingual sample PDFs, images & charts
```

---

## 🚀 Getting Started

### 1. Prerequisites (Windows 11)
- **Python**: 3.12+ (or 3.13)
- **Node.js**: v18+ (for frontend tests)
- **Git**: For version control testing

### 2. Virtual Environment Setup
```powershell
# Create virtual environment
py -3.12 -m venv .venv
# Or using default python launcher
py -m venv .venv

# Activate virtual environment
.\.venv\Scripts\Activate.ps1

# Upgrade pip
python -m pip install --upgrade pip
```

---

## 🧪 Testing Progress & Execution Commands

| # | Technology | Status | Main Test Path | Execution Command |
|---|---|:---:|---|---|
| 01 | **Python 3.12** | ✅ | `01-programming/test_python.py` | `py 01-programming/test_python.py` |
| 02 | **FastAPI** | ✅ | `02-backend/test_fastapi.py` | `.\\.venv\\Scripts\\python 02-backend/test_fastapi.py` |
| 03 | **Pydantic** | ✅ | `02-backend/test_pydantic.py` | `.\\.venv\\Scripts\\python 02-backend/test_pydantic.py` |
| 04 | **Uvicorn** | ✅ | `02-backend/test_uvicorn.py` | `.\\.venv\\Scripts\\python 02-backend/test_uvicorn.py` |
| 05 | **Docling** | ✅ | `03-pdf-processing/test_docling.py` | `.\\.venv\\Scripts\\python 03-pdf-processing/test_docling.py` |
| 06 | **PyMuPDF** | ✅ | `03-pdf-processing/test_pymupdf.py` | `.\\.venv\\Scripts\\python 03-pdf-processing/test_pymupdf.py` |
| 07 | **Tesseract OCR** | ✅ | `04-ocr-image/test_tesseract.py` | `.\\.venv\\Scripts\\python 04-ocr-image/test_tesseract.py` |
| 08 | **OpenCV** | ✅ | `04-ocr-image/test_opencv.py` | `.\\.venv\\Scripts\\python 04-ocr-image/test_opencv.py` |
| 09 | **BGE-M3** | ✅ | `05-embeddings/test_bge_m3.py` | `.\\.venv\\Scripts\\python 05-embeddings/test_bge_m3.py` |
| 10 | **Multilingual E5** | ✅ | `05-embeddings/test_multilingual_e5.py` | `.\\.venv\\Scripts\\python 05-embeddings/test_multilingual_e5.py` |
| 11 | **Sentence Transformers** | ✅ | `05-embeddings/test_sentence_transformers.py` | `.\\.venv\\Scripts\\python 05-embeddings/test_sentence_transformers.py` |
| 12 | **PostgreSQL** | ✅ | `06-vector-database/test_postgresql.py` | `.\\.venv\\Scripts\\python 06-vector-database/test_postgresql.py` |
| 13 | **pgvector** | ✅ | `06-vector-database/test_pgvector.py` | `.\\.venv\\Scripts\\python 06-vector-database/test_pgvector.py` |
| 14 | **Local instruct LLM** | ✅ | `07-llm/test_local_llm.py` | `.\\.venv\\Scripts\\python 07-llm/test_local_llm.py` |
| 15 | **Ollama** | ✅ | `07-llm/test_ollama.py` | `.\\.venv\\Scripts\\python 07-llm/test_ollama.py` |
| 16 | **Qwen2.5-VL** | ✅ | `08-vision-ai/test_qwen_vl.py` | `.\\.venv\\Scripts\\python 08-vision-ai/test_qwen_vl.py` |
| 17 | **React** | ✅ | `09-frontend/react/RAGSearchComponent.tsx` | View component source & preview |
| 18 | **TypeScript** | ✅ | `09-frontend/typescript/test_types.ts` | `npx --yes typescript --project 09-frontend/typescript/tsconfig.json` |
| 19 | **Vite** | ✅ | `09-frontend/vite/` | `npm --prefix 09-frontend/vite run dev` |
| 20 | **Tailwind CSS** | ✅ | `09-frontend/tailwind/test_tailwind.html` | Open `test_tailwind.html` in browser |
| 21 | **PDF.js** | ✅ | `09-frontend/pdfjs/test_pdfjs.html` | Open `test_pdfjs.html` in browser |
| 22 | **pytest** | ✅ | `10-testing/test_pytest.py` | `.\\.venv\\Scripts\\pytest 10-testing/test_pytest.py -v` |
| 23 | **Postman** | ✅ | `10-testing/rag_api.postman_collection.json` | Import collection into Postman |
| 24 | **Git** | ✅ | `11-version-control/test_git.ps1` | `powershell -ExecutionPolicy Bypass -File 11-version-control/test_git.ps1` |
| 25 | **GitHub** | ✅ | `11-version-control/test_github.md` | Read CI/CD & secrets documentation |
| 26 | **Docker** | ✅ | `12-deployment/Dockerfile` | `docker compose -f 12-deployment/docker-compose.yml up -d` |
| 27 | **LangChain** | ✅ | `13-rag-framework/test_langchain.py` | `.\\.venv\\Scripts\\python 13-rag-framework/test_langchain.py` |
