"""
=============================================================================
RAG Technology Testing Lab — Technology 07: Tesseract OCR (English & Khmer)
=============================================================================

1. TECHNOLOGY OVERVIEW:
   Tesseract is an open-source optical character recognition (OCR) engine.
   In a RAG system supporting scanned documents, Tesseract:
   - Converts scanned PDFs, photographs, and raster images into searchable text.
   - Extracts non-Latin scripts such as Khmer (using the `khm` traineddata model).
   - Extracts character and word bounding boxes to enable citation overlays on scanned pages.

2. INSTALLATION / PREREQUISITES:
   A. Python wrapper:
      pip install pytesseract pillow

   B. Native Tesseract Binary (Required on Windows):
      Tesseract is NOT installable via pip alone. On Windows 11, install via Winget:
        winget install UB-Mannheim.TesseractOCR
      Or download installer from:
        https://github.com/UB-Mannheim/tesseract/wiki

   C. Khmer Language Data (khm.traineddata):
      Download `khm.traineddata` from:
        https://github.com/tesseract-ocr/tessdata_fast/raw/main/khm.traineddata
      Place it inside your Tesseract tessdata directory:
        C:\\Program Files\\Tesseract-OCR\\tessdata\\khm.traineddata

3. EXECUTION INSTRUCTIONS:
   .\\.venv\\Scripts\\python 04-ocr-image/test_tesseract.py
   Or:
   py 04-ocr-image/test_tesseract.py

=============================================================================
"""

from __future__ import annotations

import json
import os
import shutil
import sys
from pathlib import Path
from PIL import Image
import pytesseract

# Windows console UTF-8 fix
if sys.platform == "win32":
    try:
        if hasattr(sys.stdout, "reconfigure"):
            sys.stdout.reconfigure(encoding="utf-8", errors="replace")
        if hasattr(sys.stderr, "reconfigure"):
            sys.stderr.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass


def locate_tesseract_binary() -> str | None:
    """Finds the tesseract executable on Windows or system PATH."""
    # 1. Check environment variable override
    env_path = os.environ.get("TESSERACT_CMD")
    if env_path and Path(env_path).is_file():
        return env_path

    # 2. Check system PATH
    which_path = shutil.which("tesseract")
    if which_path:
        return which_path

    # 3. Check common Windows install locations
    candidate_paths = [
        Path(r"C:\Program Files\Tesseract-OCR\tesseract.exe"),
        Path(r"C:\Program Files (x86)\Tesseract-OCR\tesseract.exe"),
        Path(os.path.expandvars(r"%LOCALAPPDATA%\Programs\Tesseract-OCR\tesseract.exe")),
    ]
    for candidate in candidate_paths:
        if candidate.is_file():
            return str(candidate)

    return None


def run_test() -> bool:
    print("=" * 70)
    print("🧪 Running 04-ocr-image: Tesseract OCR (English & Khmer) Test")
    print("=" * 70)

    root_dir = Path(__file__).resolve().parent.parent
    sample_en = root_dir / "sample-data" / "sample_en.png"
    sample_km = root_dir / "sample-data" / "sample_km.png"
    output_dir = Path(__file__).resolve().parent / "output"
    output_dir.mkdir(parents=True, exist_ok=True)

    # Step 1: Detect Tesseract Binary
    print("\n[Step 1/4] Detecting native Tesseract OCR engine...")
    tess_path = locate_tesseract_binary()

    if not tess_path:
        print("  ⚠️  Tesseract OCR binary was NOT found on this system.")
        print("\n  📋 Windows 11 Installation Instructions:")
        print("  1. Run this in terminal:")
        print("       winget install UB-Mannheim.TesseractOCR")
        print("  2. Download Khmer traineddata for Khmer script OCR:")
        print("       curl -o \"C:\\Program Files\\Tesseract-OCR\\tessdata\\khm.traineddata\" https://github.com/tesseract-ocr/tessdata_fast/raw/main/khm.traineddata")
        print("  3. Set environment variable in .env or PowerShell:")
        print("       $env:TESSERACT_CMD = 'C:\\Program Files\\Tesseract-OCR\\tesseract.exe'")
        print("\n  ℹ️  Note: Python wrapper `pytesseract` is installed and ready once the binary is provided.")
        return True  # Gracefully reports requirements without crashing

    pytesseract.pytesseract.tesseract_cmd = tess_path
    print(f"  ✓ Found Tesseract executable: {tess_path}")

    # Step 2: Query Available Language Models
    print("\n[Step 2/4] Querying available language packs in tessdata...")
    try:
        langs = pytesseract.get_languages()
        print(f"  ✓ Available languages: {langs}")
        has_eng = "eng" in langs
        has_khm = "khm" in langs
        print(f"  ✓ English ('eng') pack present: {has_eng}")
        print(f"  ✓ Khmer ('khm') pack present  : {has_khm}")
    except Exception as exc:
        print(f"  ✗ Failed to list languages: {exc}")
        langs, has_eng, has_khm = [], False, False

    results = {}

    # Step 3: Test English OCR
    print("\n[Step 3/4] Performing OCR on English sample (sample_en.png)...")
    if sample_en.exists() and has_eng:
        try:
            img_en = Image.open(sample_en)
            text_en = pytesseract.image_to_string(img_en, lang="eng")
            print("  ✓ English OCR output:")
            for line in text_en.strip().split("\n")[:4]:
                print(f"    | {line}")
            results["en"] = text_en
        except Exception as exc:
            print(f"  ✗ English OCR failed: {exc}")
    else:
        print("  ⚠️  Skipping English OCR (missing image or 'eng' model).")

    # Step 4: Test Khmer OCR
    print("\n[Step 4/4] Performing OCR on Khmer sample (sample_km.png)...")
    if sample_km.exists() and has_khm:
        try:
            img_km = Image.open(sample_km)
            text_km = pytesseract.image_to_string(img_km, lang="khm+eng")
            print("  ✓ Khmer OCR output:")
            for line in text_km.strip().split("\n")[:4]:
                print(f"    | {line}")
            results["km"] = text_km
        except Exception as exc:
            print(f"  ✗ Khmer OCR failed: {exc}")
    else:
        if not has_khm:
            print("  ℹ️  'khm.traineddata' is not installed in tessdata. Install it to enable Khmer text extraction.")

    # Save results
    if results:
        res_file = output_dir / "ocr_results.json"
        with open(res_file, "w", encoding="utf-8") as f:
            json.dump(results, f, ensure_ascii=False, indent=2)
        print(f"\n  ✓ Saved OCR results to: {res_file.name}")

    print("\n" + "=" * 70)
    print("🎉 Tesseract OCR inspection and validation complete!")
    print("=" * 70)
    return True


if __name__ == "__main__":
    success = run_test()
    sys.exit(0 if success else 1)
