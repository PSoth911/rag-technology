## RAG Technology Lab · Architectural Overview

Retrieval-Augmented Generation (RAG) is a pattern that augments Large Language Models (LLMs) with verified information retrieved dynamically from an external knowledge base.

## Key Pipeline Steps:

1. Document Ingestion: Parse PDFs, OCR scans, and extract text/tables.
2. Chunking &amp; Embedding: Split text into overlapping chunks and generate vector embeddings.
3. Vector Indexing: Store embeddings in PostgreSQL pgvector or dedicated vector stores.
4. Semantic Search: Perform cosine similarity matching for inbound user queries.
5. Generation &amp; Citation: Provide grounded answers accompanied by exact page citations.

| Component       | Selected Technology      | Primary Purpose                  |
|-----------------|--------------------------|----------------------------------|
| Vector Database | PostgreSQL + pgvector    | Vector Index & Similarity Search |
| Embeddings      | BGE-M3 / Multilingual-E5 | Multilingual Representation      |
| Local LLM       | Ollama / Qwen2.5-7B      | Grounded Multilingual QA         |

## Multilingual Processing &amp; Khmer Support

Section 2: Multilingual Document Ingestion

Processing non-Latin scripts such as Khmer requires Unicode normalization (NFC) and specialized multilingual embedding models like BGE-M3 to capture semantic similarity accurately.

## Sample Reference Text (Khmer):

???????? RAG ??????????????????????????????? AI ?????????????????????????? ????????????????????????????????

## Metadata:

- Target Script: Khmer (U+1780 to U+17FF)
- OCR Engine: Tesseract with 'khm' and 'eng' traineddata
- Vision Model: Qwen2.5-VL for document chart and diagram reasoning.

<!-- image -->