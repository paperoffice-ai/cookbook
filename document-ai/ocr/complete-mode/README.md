# OCR Complete-Mode — Text + Bounding Boxes + Tables

Extract text including position data (bounding boxes), table structures, and layout information. Complete-Mode provides all available OCR data — ideal for document analysis with positional context.

## Endpoint

```
POST https://api.paperoffice.ai/latest/job/add/paperoffice_aiocr___generate
```

**Authentication:** Bearer Token (API key required)

## Parameters

| Parameter | Type | Required | Default | Description |
|---|---|---|---|---|
| `file_1` | file | **Yes** | — | Document to process (PNG, JPG, TIFF, BMP, WEBP, PDF) |
| `ocr_mode` | string | No | `text` | Must be `complete` for this recipe |
| `output_searchable_pdf` | bool | No | `false` | Generate searchable PDF alongside analysis |
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

## When to use Complete-Mode?

- **Table extraction** — Invoice line items, price lists, financial data
- **Layout analysis** — Position of text blocks on the page
- **Form recognition** — Identify fields with their coordinates
- **Document reconstruction** — Recreate original structure

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
          "ocr_text": "Text of the page...",
          "line_count": 12,
          "confidence_avg": 0.9871,
          "char_count": 456,
          "language": { "primary": "de", "confidence": 0.97 },
          "bounding_boxes": [
            {
              "text": "Invoice #2024-001",
              "x": 50, "y": 80, "w": 320, "h": 28,
              "confidence": 0.99
            }
          ],
          "tables": [
            {
              "rows": [
                ["Pos", "Description", "Quantity", "Price"],
                ["1", "Consulting", "8h", "960.00 EUR"]
              ]
            }
          ]
        }
      },
      "ocr_tier": "complete",
      "ocr_mode": "complete",
      "summary": {
        "total_pages": 1,
        "total_lines": 12,
        "total_chars": 456,
        "avg_confidence": 0.99,
        "poaiocr_extracted_fulltext": "***Page 1 of 1***\n\nInvoice #2024-001...",
        "processing_engine": "paperoffice_ai_ocr_neural_v3.0"
      }
    },
    "duration_ms": "1203.44"
  }
}
```

## Additional fields compared to Text-Mode

| Field | Description |
|-------|-------------|
| `pages.XXXXX.bounding_boxes` | Array of text blocks including position (x, y, w, h) and confidence |
| `pages.XXXXX.tables` | Detected tables as nested arrays |
| `ocr_tier` | OCR tier used (`complete`) |

## Bounding box format

Each bounding box contains:

| Field | Type | Description |
|-------|------|-------------|
| `text` | string | Recognized text in the region |
| `x`, `y` | number | Position (top left, in pixels) |
| `w`, `h` | number | Width and height (in pixels) |
| `confidence` | number | Recognition confidence (0–1) |

## See also

- [Text-Mode](../text-mode/) — Plain text only (faster)
- [Searchable PDF](../searchable-pdf/) — Generate searchable PDF
