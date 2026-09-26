# Searchable PDF — Generate searchable PDF from scans

Transform scanned PDFs and images into **searchable PDFs** with an invisible OCR text layer ("sandwich PDF"). The original document remains visually unchanged but becomes full-text searchable. Can be combined with **any OCR mode**.

## Endpoint

```
POST https://api.paperoffice.ai/latest/job/add/paperoffice_aiocr___generate
```

**Authentication:** Bearer Token required

## Parameters

| Parameter | Type | Required | Default | Description |
|---|---|---|---|---|
| `file_1` | file | **Yes** | — | Document to process (PNG, JPG, TIFF, BMP, WEBP, PDF) |
| `ocr_mode` | string | No | `text` | Any mode: `text`, `grid`, `complete` |
| `output_searchable_pdf` | bool | **Yes** | — | Must be `true` for this recipe |
| `processing_lane` | string | No | workspace default | Start-SLA: `no_sla` … `instant`. `instant` returns the result inline when it finishes in time; otherwise HTTP 202 with `job_id` — poll `GET /job/get/{job_id}` |

> **Key insight:** `output_searchable_pdf=true` is an **add-on** that works with ALL OCR modes. You get the normal OCR result (text, bounding boxes, tables — depending on mode) PLUS a downloadable searchable PDF.

## Combination matrix

| OCR mode | You get text | + bounding boxes | + tables | + searchable PDF |
|---|---|---|---|---|
| `text` + `output_searchable_pdf=true` | ✅ | — | — | ✅ |
| `grid` + `output_searchable_pdf=true` | ✅ | ✅ | — | ✅ |
| `complete` + `output_searchable_pdf=true` | ✅ | ✅ | ✅ | ✅ |

## How to run

```bash
export PAPEROFFICE_API_KEY="your_api_key"

# Bash — Result is saved as searchable_output.pdf
chmod +x example.sh && ./example.sh /path/to/file.pdf

# Bash — with custom output path
./example.sh /path/to/file.pdf /path/to/output.pdf

# Python
pip install requests
python3 example.py /path/to/file.pdf output.pdf

# Node.js (v18+)
node example.js /path/to/file.pdf output.pdf
```

## When to use Searchable PDF?

- **Archiving** — GoBD/GDPR-compliant long-term archiving with full-text search
- **DMS import** — Import searchable documents into your DMS
- **Compliance** — Preserve original layout while making it searchable
- **Scan post-processing** — Prepare paper scans for digital workflows

## Response structure

The response contains both the extracted text AND a download link for the searchable PDF:

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
          "confidence_avg": 0.9954,
          "char_count": 212,
          "language": { "primary": "en", "confidence": 0.95 }
        }
      },
      "ocr_mode": "text",
      "searchable_pdf_url": "https://api.paperoffice.ai/latest/job/download/...",
      "download_token": "abc123...",
      "summary": {
        "total_pages": 1,
        "avg_confidence": 1,
        "poaiocr_extracted_fulltext": "***Page 1 of 1***\n\nThe extracted text...",
        "processing_engine": "paperoffice_ai_ocr_neural_v3.0"
      }
    },
    "duration_ms": "892.31"
  }
}
```

## Searchable PDF fields

The PDF download URL can appear in different response locations depending on the API version:

| Field | Description |
|---|---|
| `output.searchable_pdf_url` | Direct download URL for the searchable PDF |
| `output.summary.searchable_pdf_path` | Alternative location (same URL, different path) |
| `output.download_token` | Token for download via `/job/download/{token}` |

> **Tip:** The code examples check all possible field locations automatically for maximum compatibility.

## Download the searchable PDF

```bash
curl -s "https://api.paperoffice.ai/latest/job/download/YOUR_TOKEN" \
  -H "Authorization: Bearer $PAPEROFFICE_API_KEY" \
  -o "searchable.pdf"
```

## Workflow: Scan → Archive

```
1. Upload scan (file_1)
2. OCR + searchable PDF (output_searchable_pdf=true)
3. Download searchable PDF via searchable_pdf_url
4. Store in DMS/archive → full-text search works immediately
```

## Advanced: Searchable PDF + bounding boxes

Combine searchable PDF generation with full OCR analysis:

```bash
curl -X POST "https://api.paperoffice.ai/latest/job/add/paperoffice_aiocr___generate" \
  -H "Authorization: Bearer $PAPEROFFICE_API_KEY" \
  -F "file_1=@scan.pdf" \
  -F "ocr_mode=complete" \
  -F "output_searchable_pdf=true" \
  -F "processing_lane=instant"
```

This returns:
- Full text with per-page confidence
- **Bounding boxes** for every text region
- **Tables** as structured data
- **Downloadable searchable PDF**

## Supported file formats

See [Text-Mode — Supported file formats](../text-mode/#supported-file-formats) for the complete list (PDF, PNG, JPEG, TIFF, BMP, WEBP — up to 25 MB).

## See also

- [Text-Mode](../text-mode/) — Complete OCR reference (all modes, post-processing)
- [Complete-Mode](../complete-mode/) — Text + bounding boxes + tables
- [IDP Invoice](../../idp/invoice/) — Structured invoice data (uses OCR internally)
