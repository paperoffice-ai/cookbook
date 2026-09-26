# PDF AI Split — Intelligent splitting with AI detection

Splits a multi-page PDF automatically into logical individual documents. The AI detects document boundaries (e.g., where an invoice ends and a delivery note begins) and names the sub-documents intelligently.

## Endpoint

```
POST https://api.paperoffice.ai/latest/job/add/workflow
```

**Authentication:** Bearer Token (API key required)

## Parameters

| Parameter | Type | Required | Default | Description |
|---|---|---|---|---|
| `file` | file | **Yes** | — | The PDF to split |
| `template` | string | **Yes** | — | Must be `pdf_ai_split` |
| `naming_instruction` | string | No | auto | Instruction for naming sub-documents (see examples) |
| `locale` | string | No | `de_DE` | Output language: `de_DE`, `en_US`, `es_ES`, `fr_FR`, `it_IT`, `pt_PT` — affects document_type, reasoning, and filenames |
| `document_types` | string | No | auto-detect | Restrict to specific types, comma-separated: `invoice,letter,contract` |
| `date_format` | string | No | `DD.MM.YYYY` | Date output format: `YYYY-MM-DD`, `DD.MM.YYYY`, `MM/DD/YYYY` |
| `include_document_type` | bool | No | `false` | Include `document_type` in response |
| `include_date` | bool | No | `false` | Include `date` in response |
| `include_sender` | bool | No | `false` | Include `sender` in response |
| `include_reasoning` | bool | No | `false` | Include AI reasoning for the classification |
| `processing_lane` | string | No | workspace default | Start-SLA: `no_sla` … `instant`. Inline result on 200, otherwise HTTP 202 with `job_id` |

### Controlling response detail

By default, the response only contains `suggested_filename`, `page_range`, and download links. Enable additional fields explicitly:

```bash
curl -X POST "https://api.paperoffice.ai/latest/job/add/workflow" \
  -H "Authorization: Bearer $PAPEROFFICE_API_KEY" \
  -F "file=@stack.pdf" \
  -F "template=pdf_ai_split" \
  -F "naming_instruction=Name by sender, type and date" \
  -F "locale=en_US" \
  -F "date_format=YYYY-MM-DD" \
  -F "include_document_type=true" \
  -F "include_date=true" \
  -F "include_sender=true" \
  -F "include_reasoning=true" \
  -F "processing_lane=instant"
```

### Restricting document types

Limit detection to specific types (useful for known document stacks):

```bash
-F "document_types=invoice,credit_note,delivery_note"
```

When set, the AI only classifies into the provided types. Documents that don't match any type are classified as `unknown`.

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
