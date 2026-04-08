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

## Response Structure

```json
{
  "status": "success",
  "job_id": "poai-job_900_...",
  "operation": "document_anonymize",
  "result": {
    "anonymized_pdf": [
      "https://api.paperoffice.ai/latest/job/download/ZBVXGX9A..."
    ],
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

The download URL is in `result.anonymized_pdf[0]`:

```bash
curl -s "https://api.paperoffice.ai/latest/job/download/ZBVXGX9A..." \
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
