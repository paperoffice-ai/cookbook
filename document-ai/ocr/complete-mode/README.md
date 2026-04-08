# OCR Complete-Mode — Text + Bounding Boxes + Tables

Extract text including **position data (bounding boxes)**, **table structures**, and **layout information**. Complete-Mode provides all available OCR data — ideal for document analysis with positional context.

## Endpoint

```
POST https://api.paperoffice.ai/latest/job/add/paperoffice_aiocr___generate
```

**Authentication:** Bearer Token required

## Parameters

| Parameter | Type | Required | Default | Description |
|---|---|---|---|---|
| `file_1` | file | **Yes** | — | Document to process (PNG, JPG, TIFF, BMP, WEBP, PDF) |
| `ocr_mode` | string | No | `text` | Must be `complete` for this recipe (or `grid` for boxes without tables) |
| `output_searchable_pdf` | bool | No | `false` | Additionally generate a searchable PDF (sandwich PDF) |
| `priority` | int | No | `900` | `≥ 900` = synchronous (result inline) |

## OCR modes comparison

| Feature | `text` | `grid` | `complete` |
|---|---|---|---|
| Extracted text | ✅ | ✅ | ✅ |
| Confidence scores | ✅ | ✅ | ✅ |
| Language detection | ✅ | ✅ | ✅ |
| **Bounding boxes** (x, y, w, h per word/line) | — | **✅** | **✅** |
| **Table extraction** (rows + columns) | — | — | **✅** |
| **Layout analysis** (document structure) | — | — | **✅** |
| Searchable PDF (add-on) | ✅ | ✅ | ✅ |
| Speed | Fastest | Fast | Slower |

> **`grid` vs `complete`:** Use `grid` when you only need bounding boxes without table extraction — it's faster. Use `complete` when you need tables AND bounding boxes.

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
- **Redaction** — Use bounding boxes to identify and redact specific regions

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
              "id": 0,
              "text": "Invoice #2024-001",
              "x": 50, "y": 80, "w": 320, "h": 28,
              "confidence": 0.99,
              "type": "line"
            },
            {
              "id": 1,
              "text": "Acme Corporation",
              "x": 50, "y": 120, "w": 280, "h": 24,
              "confidence": 0.98,
              "type": "line"
            }
          ],
          "tables": [
            {
              "rows": [
                ["Pos", "Description", "Quantity", "Price"],
                ["1", "Consulting", "8h", "960.00 EUR"],
                ["2", "Development", "16h", "1,920.00 EUR"]
              ],
              "bounding_box": {
                "x": 50, "y": 300, "w": 500, "h": 120
              }
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

## Bounding box format

Every recognized text region gets a bounding box with pixel coordinates:

| Field | Type | Description |
|---|---|---|
| `id` | int | Unique box index on the page (used for redaction references) |
| `text` | string | Recognized text in this region |
| `x` | int | Left edge position (pixels from left) |
| `y` | int | Top edge position (pixels from top) |
| `w` | int | Width (pixels) |
| `h` | int | Height (pixels) |
| `confidence` | float | Recognition confidence (0.0–1.0) |
| `type` | string | `word`, `line`, or `block` |

### Coordinate system

```
(0,0) ─────────────────────── x →
  │
  │    ┌─────────────┐
  │    │  x,y        │
  │    │    text      │ h
  │    │              │
  │    └─────────────┘
  │         w
  y
  ↓
```

> Coordinates are in **pixels** relative to the page image. For PDFs, the page is rendered at the OCR engine's internal resolution.

## Table format

Detected tables are returned as nested arrays:

| Field | Type | Description |
|---|---|---|
| `rows` | array | Array of arrays — each inner array is one table row |
| `bounding_box` | object | Position of the entire table on the page (x, y, w, h) |

## Additional fields compared to Text-Mode

| Field | `text` | `grid` | `complete` |
|---|---|---|---|
| `pages.XXXXX.ocr_text` | ✅ | ✅ | ✅ |
| `pages.XXXXX.bounding_boxes` | — | ✅ | ✅ |
| `pages.XXXXX.tables` | — | — | ✅ |
| `ocr_tier` | — | `grid` | `complete` |

## Add-on: Searchable PDF

Works with complete-mode too — add `output_searchable_pdf=true`:

```bash
curl -X POST "https://api.paperoffice.ai/latest/job/add/paperoffice_aiocr___generate" \
  -H "Authorization: Bearer $PAPEROFFICE_API_KEY" \
  -F "file_1=@invoice.pdf" \
  -F "ocr_mode=complete" \
  -F "output_searchable_pdf=true" \
  -F "priority=900"
```

## Use case: Bounding boxes for redaction

The bounding box IDs are directly usable for the [Anonymize](../../pdf/anonymize/) workflow:

```
1. OCR with ocr_mode=complete → get bounding_boxes with IDs
2. Select box IDs to redact (e.g. boxes containing names, IBANs)
3. Call anonymize endpoint with redact_boxes=[1, 6, 7]
```

## See also

- [Text-Mode](../text-mode/) — Plain text only (faster, no bounding boxes)
- [Searchable PDF](../searchable-pdf/) — Generate searchable PDF
- [PDF Anonymize](../../pdf/anonymize/) — Use bounding boxes for GDPR redaction
