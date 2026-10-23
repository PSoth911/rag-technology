"""
Generates a multilingual sample PDF (English and Khmer) for testing PDF extractors
(Docling, PyMuPDF, PDF.js, etc.) in the RAG Technology Lab.
"""

from __future__ import annotations
import sys
from pathlib import Path
import pymupdf

# Set output path
out_dir = Path(__file__).resolve().parent
out_dir.mkdir(parents=True, exist_ok=True)
pdf_path = out_dir / "sample.pdf"

doc = pymupdf.open()

# -------------------------------------------------------------------------
# Page 1: English RAG Concepts & Architecture
# -------------------------------------------------------------------------
page1 = doc.new_page(width=595, height=842)  # A4 size

# Draw a header banner
page1.draw_rect(pymupdf.Rect(40, 40, 555, 95), color=(0.15, 0.35, 0.75), fill=(0.15, 0.35, 0.75))
page1.insert_text(pymupdf.Point(55, 75), "RAG Technology Lab — Architectural Overview", fontsize=18, color=(1, 1, 1))

# Body text
body_en = (
    "Retrieval-Augmented Generation (RAG) is a pattern that augments Large Language Models (LLMs) "
    "with verified information retrieved dynamically from an external knowledge base.\n\n"
    "Key Pipeline Steps:\n"
    "1. Document Ingestion: Parse PDFs, OCR scans, and extract text/tables.\n"
    "2. Chunking & Embedding: Split text into overlapping chunks and generate vector embeddings.\n"
    "3. Vector Indexing: Store embeddings in PostgreSQL pgvector or dedicated vector stores.\n"
    "4. Semantic Search: Perform cosine similarity matching for inbound user queries.\n"
    "5. Generation & Citation: Provide grounded answers accompanied by exact page citations."
)
page1.insert_textbox(pymupdf.Rect(40, 115, 555, 320), body_en, fontsize=11, lineheight=1.4)

# Draw a sample table representation
page1.draw_rect(pymupdf.Rect(40, 340, 555, 470), color=(0.8, 0.8, 0.8), width=1)
page1.draw_line(pymupdf.Point(40, 375), pymupdf.Point(555, 375), color=(0.8, 0.8, 0.8))
page1.insert_text(pymupdf.Point(50, 362), "Component", fontsize=11, fontname="helv")
page1.insert_text(pymupdf.Point(200, 362), "Selected Technology", fontsize=11, fontname="helv")
page1.insert_text(pymupdf.Point(380, 362), "Primary Purpose", fontsize=11, fontname="helv")

page1.insert_text(pymupdf.Point(50, 400), "Vector Database", fontsize=10)
page1.insert_text(pymupdf.Point(200, 400), "PostgreSQL + pgvector", fontsize=10)
page1.insert_text(pymupdf.Point(380, 400), "Vector Index & Similarity Search", fontsize=10)

page1.insert_text(pymupdf.Point(50, 430), "Embeddings", fontsize=10)
page1.insert_text(pymupdf.Point(200, 430), "BGE-M3 / Multilingual-E5", fontsize=10)
page1.insert_text(pymupdf.Point(380, 430), "Multilingual Representation", fontsize=10)

page1.insert_text(pymupdf.Point(50, 460), "Local LLM", fontsize=10)
page1.insert_text(pymupdf.Point(200, 460), "Ollama / Qwen2.5-7B", fontsize=10)
page1.insert_text(pymupdf.Point(380, 460), "Grounded Multilingual QA", fontsize=10)

# Footer
page1.insert_text(pymupdf.Point(40, 800), "Document ID: DOC-RAG-2026-001 | Page 1 of 2", fontsize=9, color=(0.5, 0.5, 0.5))

# -------------------------------------------------------------------------
# Page 2: Khmer and Multilingual AI Processing
# -------------------------------------------------------------------------
page2 = doc.new_page(width=595, height=842)

page2.draw_rect(pymupdf.Rect(40, 40, 555, 95), color=(0.2, 0.55, 0.35), fill=(0.2, 0.55, 0.35))
page2.insert_text(pymupdf.Point(55, 75), "Multilingual Processing & Khmer Support", fontsize=18, color=(1, 1, 1))

body_p2 = (
    "Section 2: Multilingual Document Ingestion\n\n"
    "Processing non-Latin scripts such as Khmer requires Unicode normalization (NFC) and "
    "specialized multilingual embedding models like BGE-M3 to capture semantic similarity accurately.\n\n"
    "Sample Reference Text (Khmer):\n"
    "ប្រព័ន្ធ RAG ជួយបង្កើនសមត្ថភាពឆ្លើយសំណួររបស់ AI ដោយផ្អែកលើឯកសារយោងជាក់លាក់ និងទប់ស្កាត់ការឆ្លើយខុសពីការពិត។\n\n"
    "Metadata:\n"
    "- Target Script: Khmer (U+1780 to U+17FF)\n"
    "- OCR Engine: Tesseract with 'khm' and 'eng' traineddata\n"
    "- Vision Model: Qwen2.5-VL for document chart and diagram reasoning."
)
page2.insert_textbox(pymupdf.Rect(40, 115, 555, 400), body_p2, fontsize=11, lineheight=1.4)

# Draw a sample box diagram
page2.draw_rect(pymupdf.Rect(40, 420, 180, 500), color=(0.15, 0.35, 0.75), width=2)
page2.insert_text(pymupdf.Point(60, 465), "1. PDF Ingestion", fontsize=11)

page2.draw_line(pymupdf.Point(180, 460), pymupdf.Point(230, 460), color=(0.2, 0.2, 0.2), width=2)

page2.draw_rect(pymupdf.Rect(230, 420, 370, 500), color=(0.2, 0.55, 0.35), width=2)
page2.insert_text(pymupdf.Point(245, 465), "2. Embedding & Vector DB", fontsize=11)

page2.draw_line(pymupdf.Point(370, 460), pymupdf.Point(420, 460), color=(0.2, 0.2, 0.2), width=2)

page2.draw_rect(pymupdf.Rect(420, 420, 555, 500), color=(0.75, 0.3, 0.15), width=2)
page2.insert_text(pymupdf.Point(440, 465), "3. LLM Response", fontsize=11)

# Footer
page2.insert_text(pymupdf.Point(40, 800), "Document ID: DOC-RAG-2026-001 | Page 2 of 2", fontsize=9, color=(0.5, 0.5, 0.5))

# Save PDF
doc.save(pdf_path)
doc.close()
print(f"Generated sample PDF at: {pdf_path} ({pdf_path.stat().st_size} bytes)")
