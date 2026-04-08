# PDF Anonymize — GDPR-compliant Anonymization

Automatically anonymizes personal data in PDF documents. The AI detects sensitive information and redacts it in a GDPR-compliant manner — ideal for data sharing, archiving, or data subject access requests.

## Endpoint

```
POST https://api.paperoffice.ai/latest/job/add/workflow
```

**Authentication:** Bearer Token (API key required)

## Parameters

| Parameter | Type | Required | Default | Description |
|---|---|---|---|---|
| `file` | file | **Yes** | — | PDF or image to anonymize (**not** `file_1`!) |
| `template` | string | No | `document_anonymize` | Workflow template |
| `redact_categories` | string | No | `all` | Comma-separated categories (see below) |
| `whitelist` | string | No | — | Comma-separated terms to NEVER redact |
| `custom_redact` | string | No | — | Additional terms to ALWAYS redact |
| `custom_instructions` | string | No | — | Free-text AI instructions (e.g. "Also redact all prices") |
| `pofid` | string | No | — | Alternative to `file`: use existing DMS document by POFID |
| `priority` | int | No | `999` | `≥ 900` = synchronous (result inline) |

> **Important:** The file parameter is `file`, **not** `file_1`!

## Redaction categories

| Category | What gets redacted |
|---|---|
| `all` | Everything below (default) |
| `names` | First and last names, company contacts |
| `addresses` | Street, postal code, city, country |
| `phone` | Phone numbers, fax |
| `email` | Email addresses |
| `iban` | IBAN, BIC, account numbers |
| `tax_ids` | Tax IDs, VAT numbers |
| `dates` | Dates of birth, contract dates |
| `financial` | Amounts, prices, salaries |
| `contact` | All contact information (phone, email, fax) |
| `identity` | ID numbers, passport numbers, social security |
| `none` | Disable auto-detection (use `custom_redact` only) |

## How to run

```bash
export PAPEROFFICE_API_KEY="your_api_key"

# Bash — Redact all personal data
chmod +x example.sh && ./example.sh document.pdf

# Bash — Only specific categories
./example.sh document.pdf "names,addresses"

# Python
pip install requests
python3 example.py document.pdf
python3 example.py document.pdf "names,iban"

# Node.js (v18+)
node example.js document.pdf
node example.js document.pdf "email,phone"
```

## Two anonymization approaches

### Approach 1: Single-Step (fully automatic)

One call — the AI detects and redacts everything automatically:

```bash
curl -X POST "https://api.paperoffice.ai/latest/job/add/workflow" \
  -H "Authorization: Bearer $PAPEROFFICE_API_KEY" \
  -F "file=@document.pdf" \
  -F "template=document_anonymize" \
  -F "redact_categories=all" \
  -F "priority=999"
```

### Approach 2: Preview + Apply (two-step with human review)

**Step 1 — Preview:** AI detects PII, returns page images with highlighted redaction boxes for review:

```bash
curl -X POST "https://api.paperoffice.ai/latest/job/add/workflow" \
  -H "Authorization: Bearer $PAPEROFFICE_API_KEY" \
  -F "file=@document.pdf" \
  -F "template=document_anonymize_preview" \
  -F "redact_categories=contact" \
  -F "whitelist=PaperOffice,ACME Corp" \
  -F "priority=900"
```

The response contains per-page preview images and `redact_box_ids`:

```json
{
  "result": {
    "pages_images": {
      "00001": "https://api.paperoffice.ai/latest/job/download/..."
    },
    "detected_pii": {
      "redact_box_ids": [0, 1, 2, 3, 5, 7],
      "audit_trail": [
        { "box_id": 0, "category": "names", "text": "John Smith" },
        { "box_id": 1, "category": "phone", "text": "+49 170 1234567" }
      ]
    }
  }
}
```

**Step 2 — Apply redaction:** Send back only the boxes you want to redact:

```bash
curl -X POST "https://api.paperoffice.ai/latest/job/add/workflow" \
  -H "Authorization: Bearer $PAPEROFFICE_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "files": ["https://api.paperoffice.ai/latest/job/download/...PAGE_IMAGE_URL..."],
    "boxes_by_page": {"00001": [0, 1, 5, 7]},
    "redact_color": "#000000",
    "output_pdf": true,
    "priority": 999
  }'
```

### Step 2 parameters

| Parameter | Type | Required | Default | Description |
|---|---|---|---|---|
| `files` | array | **Yes** | — | JSON array of `pages_images` URLs from Step 1 |
| `boxes_by_page` | object | No | all boxes | JSON object: `{"00001": [0, 1, 2]}` — page number (5 digits) → array of box IDs to redact |
| `redact_color` | string | No | `#000000` | Redaction fill color (hex) |
| `output_pdf` | bool | No | `true` | `true` = output PDF, `false` = output redacted images |
| `priority` | int | No | `999` | Priority |

> **When to use 2-step?** When you need human review before redacting, when you want to selectively remove only some detected PII, or when building a UI where users can approve/reject individual redactions.

## Response Structure (Single-Step)

```json
{
  "status": "success",
  "job_id": "poai-job_900_...",
  "operation": "document_anonymize",
  "result": {
    "pages_images": {
      "00001": "https://api.paperoffice.ai/latest/job/download/..."
    },
    "detected_pii": {
      "redact_box_ids": [1, 6, 7],
      "audit_trail": [
        {
          "box_id": 1,
          "category": "addresses",
          "reason": "Contains company address"
        }
      ]
    },
    "total_steps": 5,
    "duration_ms": 10643
  }
}
```

## Downloading the result

The download URL is in `result.pages_images` (per-page image URLs) or use the combined PDF:

```bash
curl -s "https://api.paperoffice.ai/latest/job/download/RESULT_TOKEN..." \
  -H "Authorization: Bearer ${PAPEROFFICE_API_KEY}" \
  -o "anonymized.pdf"
```

## GDPR Compliance

- **Art. 17 GDPR** — Right to erasure: Anonymized documents no longer contain personal data
- **Art. 15 GDPR** — Right of access: Anonymize documents before sharing
- **Art. 25 GDPR** — Data protection by design: Automatic redaction as a technical measure
- **Audit-proof** — Redaction is permanent and irreversible

## Common use cases

- **Data subject access requests** — Share documents with third parties without personal data
- **Generate test data** — Anonymize production documents for testing/development
- **Archiving** — Redact retention-required documents after personal data retention period expires
- **Sharing with external parties** — Send anonymized contracts, invoices to consultants/auditors

## See also

- [PDF AI Split](../ai-split/) — Intelligently split PDF into parts
- [Office to PDF](../office-to-pdf/) — Convert DOCX/XLSX/PPTX to PDF
- [PDF to Office](../pdf-to-office/) — Convert PDF back to DOCX/XLSX
