"""
=============================================================================
RAG Technology Testing Lab — Technology 06: PyMuPDF (fitz)
=============================================================================

1. TECHNOLOGY OVERVIEW:
   PyMuPDF (modern import: `pymupdf`) is a blazing-fast Python binding for
   MuPDF. In a production RAG system, PyMuPDF is the primary workhorse for:
   - Rapid text and page extraction from high-volume PDF documents.
   - Extracting embedded images, vector graphics, and page renderings.
   - Bounding box extraction (`search_for`) to pinpoint exact coordinates of
     matched search terms so the frontend (e.g. PDF.js) can highlight citations.
   - Reading document metadata, table of contents (bookmarks), and page layouts.

2. INSTALLATION / PREREQUISITES:
   pip install pymupdf

3. EXECUTION INSTRUCTIONS:
   .\\.venv\\Scripts\\python 03-pdf-processing/test_pymupdf.py
   Or:
   py 03-pdf-processing/test_pymupdf.py

=============================================================================
"""

from __future__ import annotations

import json
import sys
from pathlib import Path
import pymupdf

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
    print("🧪 Running 03-pdf-processing: PyMuPDF Document Extraction Test")
    print("=" * 70)
    print(f"• PyMuPDF Version: {pymupdf.__version__}")

    root_dir = Path(__file__).resolve().parent.parent
    sample_pdf = root_dir / "sample-data" / "sample.pdf"
    output_dir = Path(__file__).resolve().parent / "output"
    output_dir.mkdir(parents=True, exist_ok=True)

    if not sample_pdf.exists():
        print(f"❌ Error: Sample PDF not found at: {sample_pdf}")
        print("Please run 'python sample-data/generate_sample_pdf.py' first.")
        return False

    all_passed = True

    # Step 1: Open Document & Read Metadata
    print("\n[Step 1/5] Opening PDF and inspecting document metadata...")
    doc = pymupdf.open(sample_pdf)
    page_count = len(doc)
    print(f"  ✓ Total Pages: {page_count}")
    print(f"  ✓ Document Format: {doc.metadata.get('format', 'PDF')}")
    if page_count < 1:
        print("  ✗ Expected at least 1 page.")
        all_passed = False
    else:
        print("  ✓ Document loaded successfully.")

    # Step 2: Extract Text by Page
    print("\n[Step 2/5] Extracting text page-by-page...")
    extracted_pages = []
    for page_idx in range(page_count):
        page = doc[page_idx]
        text = page.get_text()
        extracted_pages.append({
            "page_number": page_idx + 1,
            "char_count": len(text),
            "preview": text[:120].strip().replace("\n", " ") + "...",
            "full_text": text
        })
        print(f"  ✓ Page {page_idx + 1}: {len(text)} characters extracted.")
        print(f"    Preview: {extracted_pages[-1]['preview']}")

    # Step 3: Search Terms & Extract Bounding Boxes (for UI Citations)
    print("\n[Step 3/5] Pinpointing citation bounding boxes for terms...")
    search_terms = ["Retrieval-Augmented", "PostgreSQL", "Khmer"]
    term_locations = {}

    for term in search_terms:
        matches = []
        for page_idx in range(page_count):
            page = doc[page_idx]
            rects = page.search_for(term)
            for r in rects:
                matches.append({
                    "page": page_idx + 1,
                    "bbox": [round(coord, 2) for coord in (r.x0, r.y0, r.x1, r.y1)]
                })
        term_locations[term] = matches
        print(f"  ✓ Found '{term}' in {len(matches)} location(s): {matches}")

    if not term_locations.get("Retrieval-Augmented"):
        print("  ✗ Failed to find expected search term 'Retrieval-Augmented'")
        all_passed = False

    # Step 4: Render Page to Image Pixmap (for OCR / Vision LLM)
    print("\n[Step 4/5] Rendering Page 1 to high-resolution PNG pixmap...")
    page0 = doc[0]
    # Matrix 2x zoom produces ~144 DPI for clear OCR / Vision ingestion
    pix = page0.get_pixmap(matrix=pymupdf.Matrix(2.0, 2.0))
    rendered_image_path = output_dir / "page_1_render.png"
    pix.save(rendered_image_path)
    print(f"  ✓ Rendered dimensions: {pix.width}x{pix.height} pixels")
    print(f"  ✓ Saved image to: {rendered_image_path.name} ({rendered_image_path.stat().st_size} bytes)")
    if not rendered_image_path.exists():
        all_passed = False

    # Step 5: Save Structured JSON Output
    print("\n[Step 5/5] Saving extracted data & bounding boxes to JSON...")
    export_payload = {
        "file_name": sample_pdf.name,
        "page_count": page_count,
        "pages": extracted_pages,
        "citation_coordinates": term_locations,
    }
    json_path = output_dir / "pymupdf_extracted.json"
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(export_payload, f, ensure_ascii=False, indent=2)

    print(f"  ✓ Exported structured JSON to: {json_path.name}")
    doc.close()

    print("\n" + "=" * 70)
    if all_passed:
        print("🎉 SUCCESS: PyMuPDF technology test passed all evaluations!")
    else:
        print("❌ FAILURE: PyMuPDF test encountered issues.")
    print("=" * 70)
    return all_passed


if __name__ == "__main__":
    success = run_test()
    sys.exit(0 if success else 1)
