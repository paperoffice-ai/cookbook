# IDP with Custom Extraction Fields (Custom Fields)

Defines **custom fields** for targeted data extraction — for documents not covered by a standard collection (invoice, receipt, etc.).

## Endpoint

```
POST https://api.paperoffice.ai/latest/job/add/workflow
```

**Authentication:** Bearer Token (API key required)

## Parameters

| Parameter | Type | Required | Default | Description |
|---|---|---|---|---|
| `file_1` | file | **Yes** | — | The document to process |
| `model` | string | **Yes** | — | 9 variants: `basic`, `premium`, `ultra` + `-per`/`-per-max` for more pages (see [Model tiers](../invoice/#model-tiers-9-variants)) |
| `idp_fields` | string | **Yes** | — | JSON array of field definitions (see below) |
| `idp_collection` | string | No | — | Optional: combine with a template (e.g. `invoice`) + custom fields |
| `priority` | int | No | `900` | `≥ 900` = synchronous (result inline) |

## idp_fields syntax

`idp_fields` expects a JSON array as a string. Each field has:

| Property      | Type   | Description                                   |
|---------------|--------|-----------------------------------------------|
| `name`        | string | Unique field name (snakecase recommended)     |
| `type`        | string | `string`, `number`, `date`, or `boolean`      |
| `description` | string | Natural language description for the AI       |

### Example

```json
[
  {
    "name": "contract_number",
    "type": "string",
    "description": "Contract number in the document"
  },
  {
    "name": "cancellation_period",
    "type": "string",
    "description": "Cancellation period in months or as a date"
  },
  {
    "name": "monthly_amount",
    "type": "number",
    "description": "Monthly amount in euros"
  },
  {
    "name": "contracting_party",
    "type": "string",
    "description": "Name of the contracting party"
  }
]
```

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

## When to use custom fields vs. a collection?

| Scenario                               | Recommendation                |
|----------------------------------------|-------------------------------|
| Standard invoice                       | `idp_collection=invoice`      |
| Cash register receipt                  | `idp_collection=receipt`      |
| Contract with special clauses          | **Custom Fields**             |
| Technical specification                | **Custom Fields**             |
| Industry-specific form                 | **Custom Fields**             |
| Government notice                      | **Custom Fields**             |

## Tips

- **Description is crucial**: The more precise the `description`, the better the extraction
- Use `model=premium` or `model=ultra` for custom fields — `basic` is often insufficient
- Combinable: `idp_collection` and `idp_fields` simultaneously for standard + custom fields
- Maximum of ~50 custom fields per request recommended

## Response structure

```json
{
  "status": "success",
  "job_id": "poai-job_900_...",
  "result": {
    "pages_idp": [{
      "suggested_fields": {
        "contract_number": {
          "type": "string",
          "value": "V-2024-00815",
          "source_boxes": [3, 4],
          "source_boxes_confidence": "high"
        },
        "cancellation_period": {
          "type": "string",
          "value": "3 Monate zum Quartalsende",
          "source_boxes": [12],
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
| `type` | string | Data type matching your field definition |
| `value` | string | Extracted value |
| `source_boxes` | array | Bounding box IDs showing WHERE in the document the value was found |
| `source_boxes_confidence` | string | Extraction confidence: `high`, `medium`, `low` |

> **`source_boxes`** contains integer IDs referencing OCR bounding box positions on the page (x, y, width, height). These enable visual highlighting and targeted redaction.

### Confidence levels

| Level | Meaning | Action |
|---|---|---|
| `high` | AI is confident | Use directly |
| `medium` | Likely correct | Flag for review |
| `low` | Uncertain | Manual review required |
