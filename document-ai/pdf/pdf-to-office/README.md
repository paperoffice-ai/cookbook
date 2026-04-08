# PDF to Office — Convert PDF to DOCX, XLSX, PPTX

Converts PDF documents back to editable Office formats. Preserves tables, formatting, and layout structure.

## Endpoint

```
POST https://api.paperoffice.ai/latest/job/add/paperoffice_dataripper___pdf2office
```

**Authentication:** Bearer Token (API key required)

## Parameters

| Parameter       | Value    | Description                                    |
|-----------------|----------|------------------------------------------------|
| `files`         | File     | PDF file to convert                            |
| `output_format` | `docx`   | Target format: `docx`, `xlsx`, or `pptx`       |
| `priority`      | `500`    | **Must be async** — conversion needs processing time |

> **Important:** The parameter is `output_format` — not `target_format`.

### Supported output formats

| Format | Best for                           |
|--------|------------------------------------|
| `docx` | Text documents, contracts, reports |
| `xlsx` | Tables, invoices, financial data   |
| `pptx` | Presentations, slide decks         |

## How to run

```bash
export PAPEROFFICE_API_KEY="your_api_key"

# Bash — default: DOCX
chmod +x example.sh && ./example.sh invoice.pdf

# Bash — explicit format
./example.sh report.pdf xlsx

# Python
pip install requests
python3 example.py contract.pdf docx

# Node.js (v18+)
node example.js presentation.pdf pptx
```

## Workflow

This recipe uses **async processing** because PDF-to-Office conversion requires dedicated processing:

1. **Submit** — `POST /job/add/paperoffice_dataripper___pdf2office` → returns `job_id`
2. **Poll** — `GET /job/get/{job_id}` every 5-10 seconds until `status: "completed"`
3. **Download** — Fetch the converted file from the download URL in the result

## Response (Submit)

```json
{
  "status": "success",
  "job_id": "poai-job_500_...",
  "operation": "pdf2office",
  "eta": {
    "estimated_seconds": 75,
    "estimated_completion": "2 minutes",
    "queue_position": 5,
    "estimated_processing_time": "50s"
  }
}
```

## Response (Poll — completed)

```json
{
  "job_status": "completed",
  "job_result": {
    "status": "completed",
    "result": {
      "files": ["https://api.paperoffice.ai/latest/job/download/..."]
    }
  }
}
```

## Common use cases

- **Edit scanned contracts** — PDF → DOCX for modifications in Word
- **Extract financial tables** — PDF → XLSX for Excel analysis
- **Repurpose presentations** — PDF → PPTX to edit in PowerPoint
- **Legal review** — Convert archived PDFs back to editable format with tracked changes

## See also

- [Office to PDF](../office-to-pdf/) — Convert DOCX/XLSX/PPTX to PDF
- [PDF AI Split](../ai-split/) — Intelligently split PDFs
- [PDF Anonymize](../anonymize/) — GDPR-compliant anonymization
