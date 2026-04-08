# IDP with Custom Extraction Fields (Custom Fields)

Defines **custom fields** for targeted data extraction — for documents not covered by a standard collection (invoice, receipt, etc.).

## Endpoint

```
POST https://api.paperoffice.ai/latest/job/add/workflow
```

**Authentication:** Bearer Token (API key required)

## Parameters

| Parameter    | Value               | Description                               |
|--------------|---------------------|-------------------------------------------|
| `file_1`     | File                | The document to process                   |
| `model`      | `premium`           | Recommended for custom fields             |
| `idp_fields` | JSON string         | Array of field definitions (see below)    |
| `priority`   | `900`               | Synchronous processing (≥900)             |

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
    "name": "vertragsnummer",
    "type": "string",
    "description": "Contract number in the document"
  },
  {
    "name": "kuendigungsfrist",
    "type": "string",
    "description": "Cancellation period in months or as a date"
  },
  {
    "name": "monatlicher_betrag",
    "type": "number",
    "description": "Monthly amount in euros"
  },
  {
    "name": "vertragspartner",
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
        "vertragsnummer": {
          "type": "string",
          "value": "V-2024-00815",
          "source_boxes_confidence": "high"
        },
        "kuendigungsfrist": {
          "type": "string",
          "value": "3 Monate zum Quartalsende",
          "source_boxes_confidence": "medium"
        }
      }
    }]
  }
}
```
