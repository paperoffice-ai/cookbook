# Contract Analysis (IDP Contract)

Extracts structured data from **contracts** — contracting parties, duration, cancellation period, contract value, and key clauses.

## Endpoint

```
POST https://api.paperoffice.ai/latest/job/add/workflow
```

**Authentication:** Bearer Token (API key required)

## Parameters

| Parameter | Type | Required | Default | Description |
|---|---|---|---|---|
| `file_1` | file | **Yes** | — | PDF of the contract |
| `model` | string | **Yes** | — | 9 variants: `basic`, `premium`, `ultra` + `-per`/`-per-max` for more pages (see [Model tiers](../invoice/#model-tiers-9-variants)) |
| `idp_collection` | string | No | — | Must be `contract` for this recipe |
| `idp_fields` | string | No | — | Additional custom fields as JSON (see [Custom Fields](../custom-fields/)) |
| `priority` | int | No | `900` | `≥ 900` = synchronous (result inline) |

## How to run

```bash
export PAPEROFFICE_API_KEY="your_api_key"

# Bash
bash example.sh contract.pdf

# Python
pip install requests
python3 example.py contract.pdf

# Node.js
npm install form-data
node example.js contract.pdf
```

## Available contract fields

### Contracting parties

| Field                    | Type     | Description                          |
|--------------------------|----------|--------------------------------------|
| `_party_a_name`          | string   | Name / company of the first party    |
| `_party_a_address`       | string   | Address of the first party           |
| `_party_b_name`          | string   | Name / company of the second party   |
| `_party_b_address`       | string   | Address of the second party          |

### Contract details

| Field                    | Type     | Description                          |
|--------------------------|----------|--------------------------------------|
| `_contract_type`         | string   | Contract type (lease, service agreement, etc.) |
| `_contract_number`       | string   | Contract number / reference number   |
| `_contract_date`         | date     | Date of contract execution           |
| `_effective_date`        | date     | Contract effective date              |

### Duration & termination

| Field                    | Type     | Description                          |
|--------------------------|----------|--------------------------------------|
| `_start_date`            | date     | Contract start date                  |
| `_end_date`              | date     | Contract end date                    |
| `_duration`              | string   | Duration (e.g. "24 months")         |
| `_notice_period`         | string   | Cancellation period                  |
| `_renewal_clause`        | string   | Automatic renewal                    |

### Financial

| Field                    | Type     | Description                          |
|--------------------------|----------|--------------------------------------|
| `_contract_value`        | number   | Contract value / total sum           |
| `_monthly_payment`       | number   | Monthly payment                      |
| `_payment_terms`         | string   | Payment terms                        |
| `_currency`              | string   | Currency                             |

### Additional clauses

| Field                    | Type     | Description                          |
|--------------------------|----------|--------------------------------------|
| `_governing_law`         | string   | Governing law / jurisdiction         |
| `_confidentiality`       | string   | Confidentiality clause               |
| `_penalty_clause`        | string   | Penalty clause                       |

## Response structure

```json
{
  "status": "success",
  "job_id": "poai-job_900_...",
  "result": {
    "pages_idp": [{
      "suggested_fields": {
        "_party_a_name": {
          "type": "string",
          "value": "Acme Corporation",
          "source_boxes": [2, 3],
          "source_boxes_confidence": "high"
        },
        "_duration": {
          "type": "string",
          "value": "24 Monate",
          "source_boxes": [28],
          "source_boxes_confidence": "high"
        },
        "_notice_period": {
          "type": "string",
          "value": "3 Monate zum Quartalsende",
          "source_boxes": [35, 36],
          "source_boxes_confidence": "medium"
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
| `type` | string | Data type: `string`, `number`, `date` |
| `value` | string | Formatted value |
| `value_raw` | string | Raw value for processing |
| `source_boxes` | array | Bounding box IDs showing WHERE in the document the value was found |
| `source_boxes_confidence` | string | Extraction confidence: `high`, `medium`, `low` |

> **`source_boxes`** contains integer IDs referencing OCR bounding box positions on the page (x, y, width, height). Use these for visual highlighting in validation UIs or targeted redaction.

### Confidence levels

| Level | Meaning | Action |
|---|---|---|
| `high` | AI is confident | Use directly |
| `medium` | Likely correct | Flag for review in critical workflows |
| `low` | Uncertain | Manual review required |

## Tips

- **`model=ultra`** recommended for multi-page contracts with complex clauses
- Combine with **Custom Fields** (`idp_fields`) for industry-specific clauses
- When `source_boxes_confidence` is `"low"` → plan for manual review
- Use `source_boxes` IDs for building contract review UIs that highlight extracted clauses
