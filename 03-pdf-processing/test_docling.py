"""
=============================================================================
RAG Technology Testing Lab — Technology 05: Docling
=============================================================================

1. TECHNOLOGY OVERVIEW:
   Docling is IBM's advanced document parsing and layout understanding library.
   Unlike simple raw-text extractors, Docling uses deep learning layout models to:
   - Understand reading order across multi-column documents.
   - Accurately reconstruct tables into Markdown/HTML tables.
   - Detect formulas, code blocks, headers, and image captions.
   - Export rich Markdown representations optimized for LLM chunking in RAG pipelines.

2. INSTALLATION / PREREQUISITES:
   pip install docling

3. EXECUTION INSTRUCTIONS:
   .\\.venv\\Scripts\\python 03-pdf-processing/test_docling.py
   Or:
   py 03-pdf-processing/test_docling.py

=============================================================================
"""

from __future__ import annotations

import json
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
    print("=" * 70)
    print("🧪 Running 03-pdf-processing: Docling Structured Document Extraction Test")
    print("=" * 70)

    try:
        from docling.document_converter import DocumentConverter
        import docling
        print(f"• Docling Version: {getattr(docling, '__version__', 'available')}")
    except ImportError as e:
        print(f"❌ Error importing Docling: {e}")
        print("Please install via: pip install docling")
        return False

    root_dir = Path(__file__).resolve().parent.parent
    sample_pdf = root_dir / "sample-data" / "sample.pdf"
    output_dir = Path(__file__).resolve().parent / "output"
    output_dir.mkdir(parents=True, exist_ok=True)

    if not sample_pdf.exists():
        print(f"❌ Sample PDF not found at: {sample_pdf}")
        print("Please run 'python sample-data/generate_sample_pdf.py' first.")
        return False

    all_passed = True

    # Step 1: Initialize DocumentConverter
    print("\n[Step 1/4] Initializing Docling DocumentConverter...")
    start_init = time.perf_counter()
    try:
        converter = DocumentConverter()
        init_latency = round(time.perf_counter() - start_init, 2)
        print(f"  ✓ DocumentConverter initialized in {init_latency}s.")
    except Exception as exc:
        print(f"  ✗ Failed to initialize DocumentConverter: {exc}")
        return False

    # Step 2: Convert Document
    print(f"\n[Step 2/4] Parsing and converting '{sample_pdf.name}'...")
    start_conv = time.perf_counter()
    try:
        conv_res = converter.convert(sample_pdf)
        conv_latency = round(time.perf_counter() - start_conv, 2)
        doc = conv_res.document
        print(f"  ✓ Conversion succeeded in {conv_latency}s.")
        print(f"  ✓ Document pages: {len(doc.pages)}")
    except Exception as exc:
        print(f"  ✗ Docling conversion failed: {exc}")
        return False

    # Step 3: Export to Markdown
    print("\n[Step 3/4] Exporting parsed document to structured Markdown...")
    try:
        markdown_content = doc.export_to_markdown()
        md_path = output_dir / "docling_output.md"
        with open(md_path, "w", encoding="utf-8") as f:
            f.write(markdown_content)

        print(f"  ✓ Saved Markdown to: {md_path.name} ({len(markdown_content)} characters)")
        preview_lines = markdown_content.strip().split("\n")[:8]
        print("  ✓ Markdown Preview:")
        for line in preview_lines:
            print(f"    | {line}")

        # Check for expected content
        if "RAG" in markdown_content:
            print("  ✓ Identified key content ('RAG') in markdown structure.")
        else:
            print("  ⚠ Key text not detected in markdown output.")
    except Exception as exc:
        print(f"  ✗ Markdown export failed: {exc}")
        all_passed = False

    # Step 4: Export to Dict / JSON format
    print("\n[Step 4/4] Exporting to structured JSON dict...")
    try:
        doc_dict = doc.export_to_dict()
        json_path = output_dir / "docling_output.json"
        with open(json_path, "w", encoding="utf-8") as f:
            json.dump(doc_dict, f, ensure_ascii=False, indent=2)

        print(f"  ✓ Saved structured JSON schema to: {json_path.name}")
        body_items = doc_dict.get("body", {}).get("children", [])
        print(f"  ✓ Detected document root structural elements: {len(body_items)}")
    except Exception as exc:
        print(f"  ✗ JSON export failed: {exc}")
        all_passed = False

    print("\n" + "=" * 70)
    if all_passed:
        print("🎉 SUCCESS: Docling technology test passed all evaluations!")
    else:
        print("❌ FAILURE: Docling test encountered issues.")
    print("=" * 70)
    return all_passed


if __name__ == "__main__":
    success = run_test()
    sys.exit(0 if success else 1)
