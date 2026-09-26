# AI-OCR — Complete Reference

PaperOffice AI-OCR extracts text, bounding boxes, tables, and layout from documents. Three modes, searchable PDF generation, and post-processing endpoints for retrieving results in different formats.

## Endpoint

```
POST https://api.paperoffice.ai/latest/job/add/paperoffice_aiocr___generate
```

**Authentication:** Bearer Token required

## Parameters

| Parameter | Type | Required | Default | Description |
|---|---|---|---|---|
| `file_1` | file | **Yes** | — | Document to process (see supported formats) |
| `ocr_mode` | string | No | `text` | `text`, `grid`, `complete` (see modes comparison) |
| `output_searchable_pdf` | bool | No | `false` | Additionally generate searchable PDF (sandwich PDF) |
| `processing_lane` | string | No | workspace default | Start-SLA: `no_sla`, `sla_24h`, `sla_12h`, `sla_6h`, `sla_1h`, `instant`. `instant` returns the result inline when it finishes in time; otherwise HTTP 202 with `job_id` — poll `GET /job/get/{job_id}` |

> **Note:** The file parameter is `file_1`, **not** `file`!

## Supported file formats

| Format | Extensions | Max size | Note |
|---|---|---|---|
| PDF | `.pdf` | 25 MB | Single and multi-page |
| PNG | `.png` | 25 MB | Raster image |
| JPEG | `.jpg`, `.jpeg` | 25 MB | Raster image |
| TIFF | `.tiff`, `.tif` | 25 MB | Multi-page supported |
| BMP | `.bmp` | 25 MB | Bitmap |
| WEBP | `.webp` | 25 MB | Modern web format |

## OCR modes — full comparison

| Feature | `text` | `grid` | `complete` |
|---|---|---|---|
| Full extracted text | ✅ | ✅ | ✅ |
| Per-page text (`ocr_text`) | ✅ | ✅ | ✅ |
| Confidence scores (per page + average) | ✅ | ✅ | ✅ |
| Language detection (per page) | ✅ | ✅ | ✅ |
| Character / line counts | ✅ | ✅ | ✅ |
| **Bounding boxes** (x, y, w, h per word/line) | — | **✅** | **✅** |
| **Table extraction** (rows + columns) | — | — | **✅** |
| **Layout analysis** (document structure) | — | — | **✅** |
| `output_searchable_pdf` (add-on) | ✅ | ✅ | ✅ |
| Original image dimensions | ✅ | ✅ | ✅ |
| Processing speed | Fastest | Fast | Slower |
| Credits cost | Lowest | Medium | Highest |

## How to run

```bash
export PAPEROFFICE_API_KEY="your_api_key"

# Bash — text mode (default)
chmod +x example.sh && ./example.sh /path/to/file.pdf

# Python
pip install requests
python3 example.py /path/to/file.pdf

# Node.js (v18+)
node example.js /path/to/file.pdf
```

## Response structure — text mode

```json
{
  "status": "success",
  "job_id": "poai-job_900_...",
  "operation": "generate",
  "processing_time": "1679.6ms",
  "result": {
    "status": "completed",
    "output": {
      "pages": {
        "00001": {
          "ocr_text": "Full text of page 1...",
          "line_count": 8,
          "confidence_avg": 0.9954,
          "char_count": 212,
          "language": { "primary": "de", "confidence": 0.95 },
          "original_image_width": 1632,
          "original_image_height": 2304
        }
      },
      "ocr_mode": "text",
      "summary": {
        "total_pages": 1,
        "total_lines": 8,
        "total_chars": 212,
        "avg_confidence": 1.0,
        "poaiocr_extracted_fulltext": "***Page 1 of 1***\n\nFull text...",
        "processing_engine": "paperoffice_ai_ocr_neural_v3.0"
      }
    },
    "duration_ms": "601.71"
  }
}
```

## Response structure — grid / complete mode (bounding boxes)

With `ocr_mode=grid` or `ocr_mode=complete`, each page additionally contains:

```json
{
  "pages": {
    "00001": {
      "ocr_text": "Invoice #2024-001\nAcme Corporation...",
      "confidence_avg": 0.9871,
      "original_image_width": 1632,
      "original_image_height": 2304,
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
      ]
    }
  }
}
```

### Bounding box fields

| Field | Type | Description |
|---|---|---|
| `id` | int | Unique box index on the page (for redaction, highlighting) |
| `text` | string | Recognized text in this region |
| `x` | int | Left edge (pixels from left of page) |
| `y` | int | Top edge (pixels from top of page) |
| `w` | int | Width (pixels) |
| `h` | int | Height (pixels) |
| `confidence` | float | Recognition confidence (0.0–1.0) |
| `type` | string | `word`, `line`, or `block` |

### Coordinate system

Coordinates are in **pixels** relative to the original image dimensions (`original_image_width` × `original_image_height`):

```
(0,0) ──────────────────────── x → (original_image_width)
  │
  │    ┌─────────────┐
  │    │ (x,y)       │
  │    │    text      │ h
  │    │              │
  │    └─────────────┘
  │         w
  y
  ↓
(original_image_height)
```

## Response structure — complete mode (tables)

With `ocr_mode=complete`, tables are additionally extracted:

```json
{
  "pages": {
    "00001": {
      "tables": [
        {
          "rows": [
            ["Pos", "Description", "Qty", "Price"],
            ["1", "Consulting", "8h", "960.00 EUR"],
            ["2", "Development", "16h", "1,920.00 EUR"]
          ],
          "bounding_box": {
            "x": 50, "y": 300, "w": 500, "h": 120
          }
        }
      ]
    }
  }
}
```

## Searchable PDF (add-on for any mode)

Add `output_searchable_pdf=true` to ANY mode to also receive a downloadable searchable PDF:

```bash
curl -X POST "https://api.paperoffice.ai/latest/job/add/paperoffice_aiocr___generate" \
  -H "Authorization: Bearer $PAPEROFFICE_API_KEY" \
  -F "file_1=@scan.pdf" \
  -F "ocr_mode=text" \
  -F "output_searchable_pdf=true" \
  -F "processing_lane=instant"
```

Additional response fields:

| Field | Description |
|---|---|
| `output.searchable_pdf_url` or `output.summary.searchable_pdf_path` | Direct download URL |
| `output.download_token` | Token for `/job/download/{token}` |

## Additional OCR parameters

These optional parameters can be added to the main OCR request to control result format:

### Get structured JSON with bounding boxes

Add these parameters to your OCR job request alongside `file_1` and `ocr_mode`:

```bash
curl -X POST "https://api.paperoffice.ai/latest/job/add/paperoffice_aiocr___generate" \
  -H "Authorization: Bearer $PAPEROFFICE_API_KEY" \
  -F "file_1=@document.pdf" \
  -F "ocr_mode=text" \
  -F "locale=en_US" \
  -F "page=1" \
  -F "include_bounding_boxes=true" \
  -F "processing_lane=instant"
```

| Parameter | Type | Default | Description |
|---|---|---|---|
| `locale` | string | — | Response language: `de_DE`, `en_US`, `es_ES`, `fr_FR`, `it_IT`, `pt_PT` |
| `page` | int | all | Specific page number (1-based) |
| `include_bounding_boxes` | bool | `false` | Include word coordinates (x, y, w, h) |

### Get OCR details

Retrieve detailed OCR with customizable output format:

| Parameter | Type | Default | Description |
|---|---|---|---|
| `page` | int | all | Specific page number |
| `include_bounding_boxes` | bool | `false` | Include word/line bounding boxes |
| `format` | string | `full` | `full` (all data), `text_only` (text only), `structured` (structured blocks) |

### Get plain text

Retrieve just the extracted text:

| Parameter | Type | Default | Description |
|---|---|---|---|
| `format` | string | `json` | `json` (default) or `text` (plain text without JSON wrapper) |

### Get OCR for DMS documents

For documents already stored in the PaperOffice DMS:

```
GET https://api.paperoffice.ai/latest/documents/ocr-get?pofid=YOUR_POFID
```

| Parameter | Type | Required | Description |
|---|---|---|---|
| `pofid` | string | **Yes** | PaperOffice File ID |
| `locale` | string | No | Response language |
| `page` | int | No | Specific page |
| `include_bounding_boxes` | bool | No | Include bounding boxes |

## All response fields reference

### Per-page fields

| Field | Modes | Description |
|---|---|---|
| `ocr_text` | all | Full text of the page |
| `line_count` | all | Number of text lines |
| `char_count` | all | Number of characters |
| `confidence_avg` | all | Average confidence (0–1) |
| `language.primary` | all | Detected language code |
| `language.confidence` | all | Language detection confidence |
| `original_image_width` | all | Page image width in pixels |
| `original_image_height` | all | Page image height in pixels |
| `processing_time` | all | Processing time for this page (seconds) |
| `bounding_boxes` | grid, complete | Array of positioned text regions |
| `tables` | complete | Array of detected tables |

### Summary fields

| Field | Description |
|---|---|
| `total_pages` | Total number of pages processed |
| `total_lines` | Total lines across all pages |
| `total_chars` | Total characters across all pages |
| `avg_confidence` | Average confidence across all pages |
| `poaiocr_extracted_fulltext` | Complete text with page markers (`***Page X of Y***`) |
| `processing_engine` | OCR engine version |

## Use cases by mode

| Use case | Recommended mode |
|---|---|
| Full-text search / indexing | `text` |
| AI/LLM input (embeddings, RAG) | `text` |
| Quick extraction, batch processing | `text` |
| Redaction (need box positions) | `grid` or `complete` |
| Form field extraction (coordinates) | `grid` |
| Invoice table extraction | `complete` |
| Document reconstruction / layout | `complete` |
| Archiving (searchable PDF) | any + `output_searchable_pdf=true` |

## See also

- [Complete-Mode recipe](../complete-mode/) — Focused on table + bounding box extraction
- [Searchable PDF recipe](../searchable-pdf/) — Focused on generating searchable PDFs
- [IDP Invoice](../../idp/invoice/) — Structured invoice data (uses OCR internally)
- [PDF Anonymize](../../pdf/anonymize/) — Use bounding box IDs for targeted redaction
