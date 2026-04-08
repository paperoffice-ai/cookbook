# PDF AI Split — Intelligent splitting with AI detection

Splits a multi-page PDF automatically into logical individual documents. The AI detects document boundaries (e.g., where an invoice ends and a delivery note begins) and names the sub-documents intelligently.

## Endpoint

```
POST https://api.paperoffice.ai/latest/job/add/workflow
```

**Authentication:** Bearer Token (API key required)

## Parameters

| Parameter             | Value             | Description                                     |
|-----------------------|-------------------|-------------------------------------------------|
| `file_1`              | File              | The PDF to split                                |
| `template`            | `pdf_ai_split`    | Workflow template for AI split                  |
| `naming_instruction`  | Text              | Instruction for naming sub-documents            |
| `priority`            | `900`             | Synchronous processing (≥900 = immediate)       |

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

## naming_instruction — Examples

| Instruction | Result |
|-------------|--------|
| `Name by document type and date` | `Invoice_2024-03-15_Acme_Corp.pdf` |
| `Use invoice number as filename` | `RE-2024-00142.pdf` |
| `Name by sender and type` | `Telekom_Invoice.pdf` |
| `Number sequentially with prefix SCAN` | `SCAN_001.pdf` |

## Response structure

```json
{
  "status": "success",
  "job_id": "poai-job_900_...",
  "operation": "pdf_ai_split",
  "result": {
    "documents": [
      {
        "suggested_filename": "Invoice_2024-03-15_Acme_Corp.pdf",
        "document_type": "Invoice",
        "page_range": "1-3",
        "pages": 3,
        "date": "2024-03-15",
        "sender": "Acme Corp.",
        "reasoning": "The document is an invoice from Acme Corp..."
      }
    ],
    "files": [
      "https://api.paperoffice.ai/latest/job/download/ZBVXGX9A..."
    ],
    "duration_ms": 4610
  }
}
```

## Downloading sub-documents

The download URLs are in `result.files[]` — one URL per document in `result.documents[]`:

```bash
curl -s "https://api.paperoffice.ai/latest/job/download/ZBVXGX9A..." \
  -H "Authorization: Bearer ${PAPEROFFICE_API_KEY}" \
  -o "Invoice_2024-03-15.pdf"
```

## Key fields per document

| Field                 | Description                                           |
|-----------------------|-------------------------------------------------------|
| `suggested_filename`  | AI-generated filename based on naming_instruction     |
| `document_type`       | Detected document type (invoice, contract, etc.)      |
| `page_range`          | Page range in the original document                   |
| `pages`               | Number of pages                                       |
| `date`                | Detected document date                                |
| `sender`              | Detected sender/issuer                                |
| `reasoning`           | AI reasoning for the classification                   |

## Common use cases

- **Digitize incoming mail** — Split scanned stacks into individual documents
- **Invoice processing** — Separate bulk PDFs from suppliers into individual invoices
- **Contract management** — Split multi-page contract packages into individual contracts
- **Archiving** — Automatically categorize and name large scan batches

## See also

- [PDF Anonymize](../anonymize/) — GDPR-compliant anonymization
- [Office to PDF](../office-to-pdf/) — Convert DOCX/XLSX/PPTX to PDF
- [PDF to Office](../pdf-to-office/) — Convert PDF back to DOCX/XLSX
