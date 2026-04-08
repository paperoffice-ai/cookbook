# Receipt Extraction (IDP Receipt)

Extracts structured data from **receipts and till slips** — store name, amount, date, payment method, and line items.

## Endpoint

```
POST https://api.paperoffice.ai/latest/job/add/workflow
```

**Authentication:** Bearer Token (API key required)

## Parameters

| Parameter | Type | Required | Default | Description |
|---|---|---|---|---|
| `file_1` | file | **Yes** | — | Photo or scan of the receipt |
| `model` | string | **Yes** | — | `basic` (OCR+Vision), `premium` (+AI Thinking), `ultra` (+AI Reasoning) |
| `idp_collection` | string | No | — | Must be `receipt` for this recipe |
| `idp_fields` | string | No | — | Additional custom fields as JSON (see [Custom Fields](../custom-fields/)) |
| `priority` | int | No | `900` | `≥ 900` = synchronous (result inline) |

## How to run

```bash
export PAPEROFFICE_API_KEY="your_api_key"

# Bash
bash example.sh receipt.pdf

# Python
pip install requests
python3 example.py receipt.pdf

# Node.js
npm install form-data
node example.js receipt.pdf
```

## Available receipt fields

| Field                    | Type     | Description                          |
|--------------------------|----------|--------------------------------------|
| `_store_name`            | string   | Store name / branch                  |
| `_store_address`         | string   | Store address                        |
| `_store_phone`           | string   | Phone number                         |
| `_receipt_date`          | date     | Purchase date                        |
| `_receipt_time`          | string   | Purchase time                        |
| `_receipt_number`        | string   | Receipt number / transaction number  |
| `_total_amount`          | number   | Total amount                         |
| `_net_amount`            | number   | Net amount                           |
| `_vat_amount`            | number   | VAT amount                           |
| `_vat_rate`              | number   | VAT rate                             |
| `_payment_method`        | string   | Payment method (cash, card, etc.)    |
| `_card_last_four`        | string   | Last 4 digits of the card            |
| `_currency`              | string   | Currency                             |
| `_cashier`               | string   | Cashier / attendant                  |
| `_line_items`            | table    | Individual line items                |

## Response structure

```json
{
  "status": "success",
  "job_id": "poai-job_900_...",
  "result": {
    "pages_idp": [{
      "suggested_fields": {
        "_store_name": {
          "type": "string",
          "value": "REWE Markt GmbH",
          "source_boxes": [0, 1],
          "source_boxes_confidence": "high"
        },
        "_total_amount": {
          "type": "number",
          "value": "23,47",
          "value_raw": "23.47",
          "source_boxes": [15],
          "source_boxes_confidence": "high"
        },
        "_payment_method": {
          "type": "string",
          "value": "EC-Karte",
          "source_boxes": [18],
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
| `type` | string | Data type: `string`, `number`, `date`, `table` |
| `value` | string | Formatted value (e.g. `"23,47"`) |
| `value_raw` | string | Raw value for processing (e.g. `"23.47"`) |
| `source_boxes` | array | Bounding box IDs showing WHERE in the document the value was found |
| `source_boxes_confidence` | string | Extraction confidence: `high`, `medium`, `low` |

> **`source_boxes`** contains integer IDs referencing OCR bounding box positions on the page (x, y, width, height). Use these for visual highlighting in validation UIs or targeted redaction.

### Confidence levels

| Level | Meaning | Action |
|---|---|---|
| `high` | AI is confident | Use directly |
| `medium` | Likely correct | Flag for review in critical workflows |
| `low` | Uncertain | Manual review required |

## Common use cases

- **Expense reporting**: Automatic capture of receipts
- **Accounting**: Receipt processing for small amounts
- **Travel expense reports**: Hotel and restaurant receipts
- **Expense tracking**: Categorize personal or business expenses
