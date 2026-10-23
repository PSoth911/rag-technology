# RAG Technology Testing Lab — Master Prompt

You are a Senior AI Engineer and Full-Stack Developer.

I am developing a Retrieval-Augmented Generation (RAG) system that supports PDF documents, Khmer and English text, semantic search, document citations, and visual understanding of charts, tables, and diagrams.

Before building the complete system, I want to experiment with every technology independently to understand how it works, how to configure it, and whether it is suitable for my project.

## Objective

Create a project called `rag-technology-lab` where each technology has its own independent testing file or minimal runnable module.

Do NOT build the complete RAG system yet. This project is only for learning, experimenting, and validating individual technologies.

## Technologies to test

1. Python 3.12 — Basic Python functionality, files, and data structures.
2. FastAPI — Create simple GET and POST endpoints.
3. Pydantic — Validate request and response data.
4. Uvicorn — Run the FastAPI application.
5. Docling — Extract structured content from PDF documents.
6. PyMuPDF — Extract PDF text, metadata, pages, and images.
7. Tesseract OCR — Extract Khmer and English text from images.
8. OpenCV — Perform image preprocessing, grayscale conversion, and thresholding.
9. BGE-M3 — Generate multilingual text embeddings.
10. Multilingual E5 — Generate embeddings and compare semantic similarity.
11. Sentence Transformers — Load embedding models and encode text.
12. PostgreSQL — Test database connections and CRUD operations.
13. pgvector — Store vectors and perform similarity searches.
14. Local instruct LLM — Test question answering using a local language model.
15. Ollama — Run and interact with local models through its API.
16. Qwen2.5-VL — Test image understanding, charts, and diagrams.
17. React — Build a simple interactive component.
18. TypeScript — Test interfaces, types, and typed functions.
19. Vite — Run a minimal frontend development environment.
20. Tailwind CSS — Test utility classes and responsive styling.
21. PDF.js — Display a PDF and navigate between pages.
22. pytest — Write and execute automated Python tests.
23. Postman — Create an API testing collection.
24. Git — Test repository initialization, commits, and branches.
25. GitHub — Test remote repository integration.
26. Docker — Containerize a simple application.
27. LangChain — Test document loading, chunking, and retrieval.

## Project structure

Organize the project into folders by category. Create one main testing file for each technology whenever technically possible.

For technologies that require configuration files, a running service, or a minimal project structure, create only the additional files necessary to make the test executable.

Example:

```text
rag-technology-lab/
│
├── 01-programming/
│   └── test_python.py
│
├── 02-backend/
│   ├── test_fastapi.py
│   ├── test_pydantic.py
│   └── test_uvicorn.py
│
├── 03-pdf-processing/
│   ├── test_docling.py
│   └── test_pymupdf.py
│
├── 04-ocr-image/
│   ├── test_tesseract.py
│   └── test_opencv.py
│
├── 05-embeddings/
│   ├── test_bge_m3.py
│   ├── test_multilingual_e5.py
│   └── test_sentence_transformers.py
│
├── 06-vector-database/
│   ├── test_postgresql.py
│   └── test_pgvector.py
│
├── 07-llm/
│   ├── test_local_llm.py
│   └── test_ollama.py
│
├── 08-vision-ai/
│   └── test_qwen_vl.py
│
├── 09-frontend/
│   ├── react/
│   ├── typescript/
│   ├── vite/
│   ├── tailwind/
│   └── pdfjs/
│
├── 10-testing/
│   ├── test_pytest.py
│   └── rag_api.postman_collection.json
│
├── 11-version-control/
│   ├── test_git.sh
│   └── test_github.md
│
├── 12-deployment/
│   └── Dockerfile
│
├── 13-rag-framework/
│   └── test_langchain.py
│
├── sample-data/
│   ├── sample.pdf
│   ├── sample_en.png
│   ├── sample_km.png
│   └── sample_chart.png
│
├── requirements.txt
├── .env.example
├── .gitignore
└── README.md
```

## Requirements for every technology test

Each testing file should demonstrate the technology's core functionality using the smallest practical working example.

Include:

1. **Technology overview:** Explain what the technology does and why it is relevant to a RAG system.
2. **Installation:** Provide the commands needed to install dependencies.
3. **Test implementation:** Write complete, executable code, not pseudocode.
4. **Sample input:** Use realistic examples, preferably related to PDF documents or RAG.
5. **Expected output:** Show what successful execution should look like.
6. **Execution instructions:** Explain how to run the test from the terminal.
7. **Error handling:** Handle common errors such as missing models, unavailable services, or missing files.
8. **Explanation:** Explain important functions and how the test works.
9. **Evaluation:** Explain how to determine whether the technology works correctly.
10. **RAG relevance:** Describe where the technology would be used in the future RAG architecture.

## Additional requirements

- Use Python 3.12 for Python examples.
- Support Windows 11 development.
- Prefer free, open-source, and locally runnable technologies.
- Use a Python virtual environment.
- Use environment variables for configuration and credentials.
- Do not hardcode passwords or API keys.
- Include Khmer and English examples for multilingual technologies.
- Explain when a model download, PostgreSQL server, Ollama server, or external application is required.
- Use actual model identifiers and compatible APIs.
- Do not assume that every technology is installable through pip.
- Do not invent successful execution results.
- Avoid unnecessarily complex abstractions.
- Keep every experiment independent whenever possible.
- Use modern, compatible library APIs and avoid deprecated functions.
- For hardware-intensive tests, provide CPU-compatible alternatives or explain the minimum hardware requirements.
- Include sample-data generation scripts where useful.
- Ensure tests do not overwrite important files or delete existing databases.

## Implementation workflow

Do not generate all technologies at once.

Work through the technologies one by one, starting with Python and continuing in the order listed above.

For each technology:

1. Explain its purpose.
2. Show the installation commands.
3. Generate the complete test file.
4. Show how to run it.
5. Explain the expected output.
6. Describe common errors.
7. Explain how it connects to RAG.

Wait for my confirmation before proceeding to the next technology.

Start by creating the initial project structure and implementing `01-programming/test_python.py`.