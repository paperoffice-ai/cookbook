# OCR Text-Mode — Plain text, fastest mode

Extract plain text from PDFs, images, or scans. Text-Mode is the fastest OCR mode — ideal when only the text content is needed, without layout or position data.

## Endpoint

```
POST https://api.paperoffice.ai/latest/job/add/paperoffice_aiocr___generate
```

**Authentication:** Bearer Token required

## Parameters

| Parameter | Type | Required | Default | Description |
|---|---|---|---|---|
| `file_1` | file | **Yes** | — | Document to process (see supported formats) |
| `ocr_mode` | string | No | `text` | `text` (this recipe), `grid`, `complete` |
| `output_searchable_pdf` | bool | No | `false` | Additionally generate a searchable PDF (sandwich PDF) |
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

## OCR modes comparison

All three modes use the same endpoint and `file_1` parameter. The difference is what data you get back:

| Feature | `text` | `grid` | `complete` |
|---|---|---|---|
| Extracted text | ✅ | ✅ | ✅ |
| Per-page text | ✅ | ✅ | ✅ |
| Confidence scores | ✅ | ✅ | ✅ |
| Language detection | ✅ | ✅ | ✅ |
| **Bounding boxes** (word/line positions) | — | **✅** | **✅** |
| **Table extraction** | — | — | **✅** |
| **Layout analysis** | — | — | **✅** |
| Searchable PDF (add-on) | ✅ | ✅ | ✅ |
| Speed | Fastest | Fast | Slower |

> **Tip:** Set `output_searchable_pdf=true` on ANY mode to also get a downloadable searchable PDF.

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

> Need bounding boxes? Use [Grid-Mode or Complete-Mode](../complete-mode/) instead.

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
|---|---|
| `summary.poaiocr_extracted_fulltext` | Full text of all pages (with page markers) |
| `pages.XXXXX.ocr_text` | Text of a single page |
| `pages.XXXXX.confidence_avg` | Recognition confidence (0–1) |
| `pages.XXXXX.language.primary` | Detected language of the page |
| `summary.avg_confidence` | Average confidence across all pages |
| `summary.processing_engine` | OCR engine used |

## Add-on: Searchable PDF

Add `output_searchable_pdf=true` to also receive a downloadable searchable PDF:

```bash
curl -X POST "https://api.paperoffice.ai/latest/job/add/paperoffice_aiocr___generate" \
  -H "Authorization: Bearer $PAPEROFFICE_API_KEY" \
  -F "file_1=@scan.pdf" \
  -F "ocr_mode=text" \
  -F "output_searchable_pdf=true" \
  -F "priority=900"
```

The response will include additional fields:

| Field | Description |
|---|---|
| `output.searchable_pdf_url` | Direct download URL for the searchable PDF |
| `output.download_token` | Token for download via `/job/download/{token}` |

See [Searchable PDF recipe](../searchable-pdf/) for full details.

## See also

- [Complete-Mode](../complete-mode/) — Text + **bounding boxes** + tables + layout
- [Searchable PDF](../searchable-pdf/) — Generate searchable PDF from scans
- [IDP Invoice](../../idp/invoice/) — Structured invoice data extraction (uses OCR internally)
