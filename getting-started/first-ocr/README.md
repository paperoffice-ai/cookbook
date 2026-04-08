# First OCR Call — Text Extraction

Extract text from a document (PDF, image, scan) with PaperOffice AI OCR.

## Endpoint

```
POST https://api.paperoffice.ai/latest/job/add/paperoffice_aiocr___generate
```

**Authentication:** Bearer Token (API key required)

## Parameters

| Parameter  | Value    | Description                           |
|-----------|----------|---------------------------------------|
| `file_1`  | File     | The document to process               |
| `ocr_mode`| `text`   | Extract text only (no layout)         |
| `priority`| `900`    | Synchronous processing (immediate)    |

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
  "result": {
    "output": {
      "summary": {
        "poaiocr_extracted_fulltext": "The full extracted text...",
        "total_pages": 1,
        "total_lines": 42,
        "avg_confidence": 0.97
      },
      "pages": {
        "00001": {
          "ocr_text": "Text of the first page..."
        }
      }
    }
  }
}
```

## Priority system

| Priority | Behavior                                       |
|---------|------------------------------------------------|
| `900`   | **Synchronous** — Result directly in the response |
| `500`   | **Async** — Returns `job_id` for polling        |
| `100`   | **Low** — Background processing                 |

For synchronous results (as in this example) always use `priority=900`.
