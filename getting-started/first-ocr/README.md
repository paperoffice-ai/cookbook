# First OCR Call — Text Extraction

Extract text from a document (PDF, image, scan) with PaperOffice AI OCR.

## Endpoint

```
POST https://api.paperoffice.ai/latest/job/add/paperoffice_aiocr___generate
```

**Authentication:** Bearer Token (API key required)

## Parameters

| Parameter | Type | Required | Default | Description |
|---|---|---|---|---|
| `file_1` | file | **Yes** | — | Document to process (PDF, PNG, JPG, TIFF, BMP, WEBP) |
| `ocr_mode` | string | No | `text` | `text` (fastest), `grid` (+ bounding boxes), `complete` (+ tables + layout) |
| `priority` | int | No | `900` | `≥ 900` = synchronous (result inline) |

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

## Response structure

```json
{
  "status": "success",
  "job_id": "poai-job_900_...",
  "result": {
    "status": "completed",
    "output": {
      "summary": {
        "poaiocr_extracted_fulltext": "***Page 1 of 1***\n\nThe full extracted text...",
        "total_pages": 1,
        "total_lines": 42,
        "avg_confidence": 0.97,
        "processing_engine": "paperoffice_ai_ocr_neural_v3.0"
      },
      "pages": {
        "00001": {
          "ocr_text": "Text of the first page...",
          "confidence_avg": 0.97,
          "char_count": 212,
          "language": { "primary": "en", "confidence": 0.95 }
        }
      },
      "ocr_mode": "text"
    },
    "duration_ms": "601.71"
  }
}
```

### Key fields

| Field | Description |
|---|---|
| `summary.poaiocr_extracted_fulltext` | Full text of all pages (with page markers) |
| `pages.00001.ocr_text` | Text of a single page |
| `summary.avg_confidence` | Average recognition confidence (0–1) |

## Priority system

| Priority | Behavior                                       |
|---------|------------------------------------------------|
| `900`   | **Synchronous** — Result directly in the response |
| `500`   | **Async** — Returns `job_id` for polling        |
| `100`   | **Low** — Background processing                 |

For synchronous results (as in this example) always use `priority=900`.
