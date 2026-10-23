"""
=============================================================================
RAG Technology Testing Lab — Technology 08: OpenCV (Image Preprocessing)
=============================================================================

1. TECHNOLOGY OVERVIEW:
   OpenCV (Open Source Computer Vision) is the industry-standard computer vision
   library. In a multimodal RAG system handling scanned PDFs and diagrams, OpenCV:
   - Cleans scanned images (deskewing, noise reduction, shadow removal).
   - Binarizes document scans using Otsu and adaptive thresholding to maximize OCR accuracy.
   - Detects contours and bounding boxes for tables, figures, charts, and text blocks.
   - Crops visual components for specialized vision models (like Qwen2.5-VL).

2. INSTALLATION:
   pip install opencv-python-headless pillow numpy

3. EXECUTION INSTRUCTIONS:
   .\\.venv\\Scripts\\python 04-ocr-image/test_opencv.py
   Or:
   py 04-ocr-image/test_opencv.py

=============================================================================
"""

from __future__ import annotations

import sys
from pathlib import Path
import cv2
import numpy as np

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
    print("🧪 Running 04-ocr-image: OpenCV Preprocessing Test")
    print("=" * 70)
    print(f"• OpenCV Version: {cv2.__version__}")

    root_dir = Path(__file__).resolve().parent.parent
    sample_chart = root_dir / "sample-data" / "sample_chart.png"
    sample_en = root_dir / "sample-data" / "sample_en.png"
    output_dir = Path(__file__).resolve().parent / "output"
    output_dir.mkdir(parents=True, exist_ok=True)

    if not sample_chart.exists() or not sample_en.exists():
        print("❌ Error: Sample images not found in sample-data/.")
        print("Please run: python sample-data/generate_sample_images.py")
        return False

    all_passed = True

    # Step 1: Load Image & Inspect Matrix Properties
    print("\n[Step 1/5] Loading sample image and checking matrix dimensions...")
    img = cv2.imread(str(sample_chart))
    if img is None:
        print("  ✗ Failed to load image via cv2.imread.")
        return False

    h, w, channels = img.shape
    print(f"  ✓ Image loaded: {w}x{h} px, Channels: {channels}, Dtype: {img.dtype}")

    # Step 2: Grayscale Conversion
    print("\n[Step 2/5] Converting RGB to Grayscale...")
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    gray_path = output_dir / "01_grayscale.png"
    cv2.imwrite(str(gray_path), gray)
    print(f"  ✓ Saved Grayscale output: {gray_path.name}")

    # Step 3: Gaussian Denoising & Otsu Binarization (Thresholding)
    print("\n[Step 3/5] Applying Gaussian blur and Otsu automatic thresholding...")
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)
    # Otsu thresholding finds optimal threshold between foreground and background
    _, thresh = cv2.threshold(blurred, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)
    thresh_path = output_dir / "02_otsu_threshold.png"
    cv2.imwrite(str(thresh_path), thresh)
    print(f"  ✓ Saved Threshold binarization: {thresh_path.name}")

    # Step 4: Morphological Operations (Dilation for text/block grouping)
    print("\n[Step 4/5] Morphological dilation to group text and chart blocks...")
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (7, 7))
    dilated = cv2.dilate(thresh, kernel, iterations=2)
    dilated_path = output_dir / "03_dilated_blocks.png"
    cv2.imwrite(str(dilated_path), dilated)
    print(f"  ✓ Saved Dilated regions: {dilated_path.name}")

    # Step 5: Contour Detection & Bounding Box Extraction
    print("\n[Step 5/5] Extracting document structure contours and bounding boxes...")
    contours, _ = cv2.findContours(dilated, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    annotated = img.copy()

    detected_boxes = []
    min_area = 500  # Filter out minor noise dots
    for cnt in contours:
        area = cv2.contourArea(cnt)
        if area > min_area:
            x, y, bw, bh = cv2.boundingRect(cnt)
            detected_boxes.append({"x": x, "y": y, "w": bw, "h": bh, "area": int(area)})
            # Draw green bounding box around detected element
            cv2.rectangle(annotated, (x, y), (x + bw, y + bh), (0, 200, 0), 2)
            cv2.putText(
                annotated,
                f"{bw}x{bh}",
                (x, max(15, y - 5)),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.45,
                (0, 150, 0),
                1,
            )

    annotated_path = output_dir / "04_detected_contours.png"
    cv2.imwrite(str(annotated_path), annotated)
    print(f"  ✓ Detected {len(detected_boxes)} high-confidence regions/blocks.")
    print(f"  ✓ Saved Annotated image: {annotated_path.name}")

    if len(detected_boxes) == 0:
        print("  ✗ Expected at least 1 region detected.")
        all_passed = False

    print("\n" + "=" * 70)
    if all_passed:
        print("🎉 SUCCESS: OpenCV technology test passed all evaluations!")
    else:
        print("❌ FAILURE: OpenCV test encountered issues.")
    print("=" * 70)
    return all_passed


if __name__ == "__main__":
    success = run_test()
    sys.exit(0 if success else 1)
