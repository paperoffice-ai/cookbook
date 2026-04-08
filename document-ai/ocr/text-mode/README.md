# OCR Text-Mode — Plain text, fastest mode

Extract plain text from PDFs, images, or scans. Text-Mode is the fastest OCR mode — ideal when only the text content is needed, without layout or position data.

## Endpoint

```
POST https://api.paperoffice.ai/latest/job/add/paperoffice_aiocr___generate
```

**Authentication:** Bearer Token (API key required)

## Parameters

| Parameter | Type | Required | Default | Description |
|---|---|---|---|---|
| `file_1` | file | **Yes** | — | Document to process (see supported formats below) |
| `ocr_mode` | string | No | `text` | OCR mode: `text` (this recipe), `grid`, `complete` |
| `output_searchable_pdf` | bool | No | `false` | Generate searchable PDF alongside text |
| `priority` | int | No | `900` | `≥ 900` = synchronous (result inline) |

## Supported file formats

| Format | Extensions | Note |
|---|---|---|
| PDF | `.pdf` | Single and multi-page |
| PNG | `.png` | Raster image |
| JPEG | `.jpg`, `.jpeg` | Raster image |
| TIFF | `.tiff`, `.tif` | Multi-page supported |
| BMP | `.bmp` | Bitmap |
| WEBP | `.webp` | Modern web format |

## How to run

```bash
export PAPEROFFICE_API_KEY="your_api_key"

# Bash
chmod +x example.sh && ./example.sh /path/to/file.pdf

# Python
pip install requests
python3 example.py /path/to/file.pdf

# Node.js (v18+)
node example.js /path/to/file.pdf
```

## When to use Text-Mode?

- **Full-text search** — Build index for search engines
- **AI processing** — Text as input for LLMs or embeddings
- **Quick extraction** — When layout/position is irrelevant
- **Batch processing** — High throughput for many documents

## Response structure

```json
{
  "status": "success",
  "job_id": "poai-job_900_...",
  "result": {
    "status": "completed",
    "output": {
      "pages": {
        "00001": {
          "ocr_text": "Text of the first page...",
          "line_count": 8,
          "confidence_avg": 0.9954,
          "char_count": 212,
          "language": { "primary": "de", "confidence": 0.95 }
        }
      },
      "ocr_mode": "text",
      "summary": {
        "total_pages": 1,
        "total_lines": 8,
        "total_chars": 212,
        "avg_confidence": 1,
        "poaiocr_extracted_fulltext": "***Page 1 of 1***\n\nThe complete text...",
        "processing_engine": "paperoffice_ai_ocr_neural_v3.0"
      }
    },
    "duration_ms": "601.71"
  }
}
```

## Key fields

| Field | Description |
|-------|-------------|
| `summary.poaiocr_extracted_fulltext` | Full text of all pages (with page markers) |
| `pages.XXXXX.ocr_text` | Text of a single page |
| `pages.XXXXX.confidence_avg` | Recognition confidence (0–1) |
| `summary.avg_confidence` | Average confidence across all pages |
| `summary.processing_engine` | OCR engine used |

## See also

- [Complete-Mode](../complete-mode/) — Text + bounding boxes + tables
- [Searchable PDF](../searchable-pdf/) — Generate searchable PDF
