# Searchable PDF — Generate searchable PDF from scans

Transform scanned PDFs and images into searchable PDFs with an invisible text layer. Ideal for archiving — the original document remains visually unchanged but becomes full-text searchable.

## Endpoint

```
POST https://api.paperoffice.ai/latest/job/add/paperoffice_aiocr___generate
```

**Authentication:** Bearer Token (API key required)

## Parameters

| Parameter               | Value  | Description                               |
|------------------------|--------|-------------------------------------------|
| `file_1`               | File   | The document to process                   |
| `ocr_mode`             | `text` | Text extraction as basis                  |
| `output_searchable_pdf`| `true` | Additionally generate searchable PDF      |
| `priority`             | `900`  | Synchronous processing (immediate)        |

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

The response contains both the extracted text and a download link for the searchable PDF:

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
          "confidence_avg": 0.9954
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

## Additional fields

| Field | Description |
|-------|-------------|
| `output.searchable_pdf_url` | Direct download URL for the searchable PDF |
| `output.download_token` | Alternative: Token for download via `/job/download/{token}` |

## Workflow: Scan → Archive

```
1. Upload scan (file_1)
2. Generate OCR + searchable PDF (output_searchable_pdf=true)
3. Download searchable PDF
4. Store in DMS/archive → full-text search works immediately
```

## See also

- [Text-Mode](../text-mode/) — Plain text only (without PDF generation)
- [Complete-Mode](../complete-mode/) — Text + bounding boxes + tables
