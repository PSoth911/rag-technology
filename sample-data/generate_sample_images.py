"""
Generates sample images (English text, Khmer text snippet, and a synthetic bar chart)
for OCR and Vision AI testing in the RAG Technology Lab.
"""

from __future__ import annotations
import math
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

out_dir = Path(__file__).resolve().parent
out_dir.mkdir(parents=True, exist_ok=True)

# -------------------------------------------------------------------------
# 1. Sample English Document Image (sample_en.png)
# -------------------------------------------------------------------------
img_en = Image.new("RGB", (650, 300), color=(255, 255, 255))
draw_en = ImageDraw.Draw(img_en)

# Header
draw_en.rectangle([(0, 0), (650, 50)], fill=(33, 75, 140))
draw_en.text((20, 15), "RAG Document Parser — English Sample", fill=(255, 255, 255))

# Body
en_lines = [
    "Retrieval-Augmented Generation (RAG) is an architectural approach",
    "that connects external documents directly to LLM prompts.",
    "",
    "Key Technologies:",
    "• Vector Database: PostgreSQL with pgvector extension.",
    "• Embedding Model: BGE-M3 and Multilingual-E5.",
    "• OCR Engine: Tesseract with multi-script dictionaries."
]
y_offset = 70
for line in en_lines:
    draw_en.text((25, y_offset), line, fill=(20, 20, 20))
    y_offset += 28

img_en.save(out_dir / "sample_en.png")
print("Saved sample_en.png")

# -------------------------------------------------------------------------
# 2. Sample Khmer Document Image (sample_km.png)
# -------------------------------------------------------------------------
img_km = Image.new("RGB", (650, 300), color=(255, 255, 255))
draw_km = ImageDraw.Draw(img_km)

draw_km.rectangle([(0, 0), (650, 50)], fill=(40, 130, 80))
draw_km.text((20, 15), "RAG Technology Lab — Khmer Language Ingestion", fill=(255, 255, 255))

km_lines = [
    "ប្រព័ន្ធ RAG ជួយបង្កើនសមត្ថភាពឆ្លើយសំណួររបស់ AI",
    "ដោយផ្អែកលើឯកសារយោងជាក់លាក់ និងទប់ស្កាត់ការឆ្លើយខុស។",
    "",
    "បច្ចេកវិទ្យាសំខាន់ៗ (Core Technologies):",
    "• មូលដ្ឋានទិន្នន័យវ៉ិចទ័រ (Vector Database): PostgreSQL + pgvector",
    "• ម៉ូដែលបកប្រែវ៉ិចទ័រ (Embeddings): BGE-M3",
    "• ការស្រង់អត្ថបទ (OCR Engine): Tesseract OCR (khm + eng)"
]
y_offset = 70
for line in km_lines:
    draw_km.text((25, y_offset), line, fill=(20, 20, 20))
    y_offset += 28

img_km.save(out_dir / "sample_km.png")
print("Saved sample_km.png")

# -------------------------------------------------------------------------
# 3. Sample Bar Chart Diagram (sample_chart.png) for Vision LLM
# -------------------------------------------------------------------------
img_chart = Image.new("RGB", (700, 420), color=(248, 250, 252))
draw_chart = ImageDraw.Draw(img_chart)

# Title & subtitle
draw_chart.text((30, 20), "Retrieval Accuracy Comparison Across Embedding Models", fill=(15, 23, 42))
draw_chart.text((30, 45), "Metric: Mean Reciprocal Rank (MRR@10) on Multilingual Corpus", fill=(100, 116, 139))

# Draw axes
origin_x, origin_y = 100, 340
draw_chart.line([(origin_x, 80), (origin_x, origin_y)], fill=(148, 163, 184), width=2)
draw_chart.line([(origin_x, origin_y), (650, origin_y)], fill=(148, 163, 184), width=2)

# Grid lines and Y labels
for idx, val in enumerate([0, 25, 50, 75, 100]):
    y = origin_y - int(val * 2.2)
    draw_chart.line([(origin_x - 5, y), (650, y)], fill=(226, 232, 240), width=1)
    draw_chart.text((55, y - 8), f"{val}%", fill=(100, 116, 139))

# Data points: (Model name, Accuracy score %, color)
data = [
    ("BM25 (Keyword)", 52, (156, 163, 175)),
    ("MiniLM-L6", 68, (59, 130, 246)),
    ("Multilingual-E5", 84, (16, 185, 129)),
    ("BGE-M3 (Hybrid)", 91, (139, 92, 246)),
]

bar_width = 85
spacing = 45
curr_x = origin_x + 35

for label, score, color in data:
    bar_height = int(score * 2.2)
    top_y = origin_y - bar_height
    draw_chart.rectangle(
        [(curr_x, top_y), (curr_x + bar_width, origin_y)],
        fill=color,
        outline=(30, 41, 59),
        width=1
    )
    # Score label on top of bar
    draw_chart.text((curr_x + 22, top_y - 20), f"{score}%", fill=(15, 23, 42))
    # X label below bar
    draw_chart.text((curr_x - 5, origin_y + 15), label, fill=(30, 41, 59))
    curr_x += bar_width + spacing

img_chart.save(out_dir / "sample_chart.png")
print("Saved sample_chart.png")
