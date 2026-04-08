# Office to PDF — Convert Office Documents to PDF

Converts Office documents (DOCX, XLSX, PPTX, etc.) to PDF using **native Microsoft Office** on a Windows VM. This ensures pixel-perfect conversion with full layout fidelity — unlike LibreOffice-based converters.

## Endpoint

```
POST https://api.paperoffice.ai/latest/job/add/paperoffice_dataripper___office2pdf
```

**Authentication:** Bearer Token (API key required)

## Parameters

| Parameter  | Value     | Description                                              |
|------------|-----------|----------------------------------------------------------|
| `files`    | File      | Office document to convert                               |
| `provider` | `native`  | Conversion engine (see below)                            |
| `priority` | `500`     | **Must be async** — native conversion requires a Windows VM |

### Provider options

| Provider  | Engine                          | Quality     | Speed    |
|-----------|---------------------------------|-------------|----------|
| `native`  | Windows VM + real MS Office     | **Best**    | ~30-90s  |
| `adobe`   | Adobe Cloud                     | Excellent   | ~20-60s  |

### Supported input formats

**DOCX**, DOC, **XLSX**, XLS, **PPTX**, PPT, PPS, ODS, ODT, ODP, RTF

## How to run

```bash
export PAPEROFFICE_API_KEY="your_api_key"

# Bash
chmod +x example.sh && ./example.sh report.docx

# Bash with provider
./example.sh spreadsheet.xlsx adobe

# Python
pip install requests
python3 example.py contract.docx

# Node.js (v18+)
node example.js presentation.pptx
```

## Workflow

This recipe uses **async processing** because native MS Office conversion runs on a dedicated Windows VM:

1. **Submit** — `POST /job/add/paperoffice_dataripper___office2pdf` → returns `job_id`
2. **Poll** — `GET /job/get/{job_id}` every 5-10 seconds until `status: "completed"`
3. **Download** — Fetch the PDF from the download URL in the result

## Response (Submit)

```json
{
  "status": "success",
  "job_id": "poai-job_500_...",
  "operation": "office2pdf",
  "eta": {
    "estimated_seconds": 55,
    "estimated_completion": "55 seconds",
    "queue_position": 3,
    "estimated_processing_time": "30s"
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

## Why native MS Office?

| Feature                  | Native MS Office | LibreOffice   |
|--------------------------|------------------|---------------|
| Font rendering           | Perfect          | Approximate   |
| Complex tables           | Exact            | Often broken  |
| Charts & SmartArt        | Full support     | Partial       |
| Embedded macros/VBA      | Handled          | Ignored       |
| Header/Footer            | Pixel-perfect    | Shifted       |
| Page breaks              | Exact            | Different     |

## Common use cases

- **Contract archiving** — Convert signed DOCX contracts to archival PDF
- **Financial reports** — XLSX spreadsheets to print-ready PDF
- **Presentations** — PPTX to PDF for email distribution
- **Legal documents** — Preserve exact formatting for compliance

## See also

- [PDF to Office](../pdf-to-office/) — Convert PDF back to DOCX/XLSX
- [PDF AI Split](../ai-split/) — Intelligently split PDFs
- [PDF Anonymize](../anonymize/) — GDPR-compliant anonymization
