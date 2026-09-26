# Identity Document Extraction (IDP Identity)

Extracts structured data from **ID cards, passports, and driver's licenses** — name, date of birth, document number, expiry date, nationality, and more.

## Endpoint

```
POST https://api.paperoffice.ai/latest/job/add/workflow
```

**Authentication:** Bearer Token (API key required)

## Parameters

| Parameter | Type | Required | Default | Description |
|---|---|---|---|---|
| `file_1` | file | **Yes** | — | Scan or photo of the ID document |
| `model` | string | **Yes** | — | 9 variants: `basic`, `premium`, `ultra` + `-per`/`-per-max` for more pages (see [Model tiers](../invoice/#model-tiers-9-variants)) |
| `idp_collection` | string | No | — | Must be `identity_document` for this recipe |
| `idp_fields` | string | No | — | Additional custom fields as JSON (see [Custom Fields](../custom-fields/)) |
| `processing_lane` | string | No | workspace default | Start-SLA: `no_sla` … `instant`. `instant` returns the result inline when it finishes in time; otherwise HTTP 202 with `job_id` — poll `GET /job/get/{job_id}` |

## How to run

```bash
export PAPEROFFICE_API_KEY="your_api_key"

# Bash
bash example.sh id_card.pdf

# Python
pip install requests
python3 example.py id_card.pdf

# Node.js
npm install form-data
node example.js id_card.pdf
```

## Available identity document fields

### Personal data

| Field                    | Type     | Description                          |
|--------------------------|----------|--------------------------------------|
| `_first_name`            | string   | First name                           |
| `_last_name`             | string   | Last name                            |
| `_full_name`             | string   | Full name                            |
| `_date_of_birth`         | date     | Date of birth                        |
| `_place_of_birth`        | string   | Place of birth                       |
| `_gender`                | string   | Gender                               |
| `_nationality`           | string   | Nationality                          |
| `_address`               | string   | Residential address (if available)   |

### Document data

| Field                    | Type     | Description                          |
|--------------------------|----------|--------------------------------------|
| `_document_type`         | string   | Type (ID card, passport, driver's license) |
| `_document_number`       | string   | Document number / serial number      |
| `_issuing_authority`     | string   | Issuing authority                    |
| `_issuing_country`       | string   | Issuing country                      |
| `_issue_date`            | date     | Issue date                           |
| `_expiry_date`           | date     | Expiry date / valid until            |

### Machine Readable Zone (MRZ)

| Field                    | Type     | Description                          |
|--------------------------|----------|--------------------------------------|
| `_mrz_line_1`            | string   | First line of the MRZ               |
| `_mrz_line_2`            | string   | Second line of the MRZ              |
| `_mrz_line_3`            | string   | Third line of the MRZ (if available)|

## Response structure

```json
{
  "status": "success",
  "job_id": "poai-job_900_...",
  "result": {
    "pages_idp": [{
      "suggested_fields": {
        "_full_name": {
          "type": "string",
          "value": "John Smith",
          "source_boxes": [3, 4],
          "source_boxes_confidence": "high"
        },
        "_document_number": {
          "type": "string",
          "value": "T220001293",
          "source_boxes": [8],
          "source_boxes_confidence": "high"
        },
        "_date_of_birth": {
          "type": "date",
          "value": "1985-03-15",
          "source_boxes": [12],
          "source_boxes_confidence": "high"
        },
        "_expiry_date": {
          "type": "date",
          "value": "2028-03-14",
          "source_boxes": [15],
          "source_boxes_confidence": "high"
        },
        "_nationality": {
          "type": "string",
          "value": "DEUTSCH",
          "source_boxes": [6],
          "source_boxes_confidence": "high"
        }
      }
    }]
  }
}
```

## Field metadata & bounding boxes

Every extracted field contains traceability metadata:

| Property | Type | Description |
|---|---|---|
| `type` | string | Data type: `string`, `date` |
| `value` | string | Extracted value |
| `source_boxes` | array | Bounding box IDs showing WHERE in the document the value was found |
| `source_boxes_confidence` | string | Extraction confidence: `high`, `medium`, `low` |

> **`source_boxes`** contains integer IDs referencing OCR bounding box positions on the page (x, y, width, height). Use these for visual highlighting in KYC verification UIs.

### Confidence levels

| Level | Meaning | Action |
|---|---|---|
| `high` | AI is confident | Use directly |
| `medium` | Likely correct | Flag for review |
| `low` | Uncertain | Manual review required |

## Common use cases

- **KYC verification**: Know Your Customer in the financial sector
- **Onboarding**: Automatic data capture during new customer registration
- **Age verification**: Automatically check date of birth
- **Expiry monitoring**: Detect documents with upcoming expiration

## Data privacy notice

Identity documents contain particularly sensitive personal data. Please note:
- Ensure GDPR-compliant processing
- Only store data for as long as necessary
- Restrict access to extracted data
- PaperOffice AI processes data on EU servers (Frankfurt)
