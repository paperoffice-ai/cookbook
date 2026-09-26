# Invoice Extraction (IDP Invoice)

Extracts **28+ structured fields** from invoices — invoice number, amounts, supplier, IBAN, line items, and more. Each field includes confidence scores and bounding boxes.

## Endpoint

```
POST https://api.paperoffice.ai/latest/job/add/workflow
```

**Authentication:** Bearer Token (API key required)

## Parameters

| Parameter | Type | Required | Default | Description |
|---|---|---|---|---|
| `file_1` | file | **Yes** | — | PDF or image of the invoice |
| `model` | string | **Yes** | — | AI tier (see model tiers below) |
| `idp_collection` | string | No | `invoice` | Template: `invoice` (English), `invoice:de` (German/DATEV), `invoice:en`, `invoice:es` |
| `idp_fields` | string | No | — | Additional custom fields as JSON (see [Custom Fields](../custom-fields/)) |
| `processing_lane` | string | No | workspace default | Start-SLA: `no_sla` … `instant`. `instant` returns the result inline when it finishes in time; otherwise HTTP 202 with `job_id` — poll `GET /job/get/{job_id}` |

## Model tiers (9 variants)

The `model` parameter controls AI intelligence AND page limits. There are 3 intelligence levels × 3 page variants:

### Intelligence levels

| Level | Description | Best for |
|---|---|---|
| `basic` | OCR + Vision | Simple, clean documents with few fields |
| `premium` | + AI Thinking | Standard documents, multi-page, line items |
| `ultra` | + AI Reasoning | Complex documents, handwritten, poor scans |

### Page variants

| Suffix | Page limit | Credits | Description |
|---|---|---|---|
| *(none)* | ~1–3 pages | Standard | Single documents (invoice, receipt, ID) |
| `-per` | ~5–10 pages | Higher | Multi-page documents (contracts, reports) |
| `-per-max` | ~20–50+ pages | Highest | Large documents (legal files, manuals) |

### All 9 model values

| Model | Intelligence | Pages | Recommended for |
|---|---|---|---|
| `basic` | OCR+Vision | 1–3 | Single-page receipts, simple forms |
| `basic-per` | OCR+Vision | 5–10 | Multi-page basic extraction |
| `basic-per-max` | OCR+Vision | 20–50+ | Large batch basic extraction |
| `premium` | +AI Thinking | 1–3 | **Standard invoices** (recommended default) |
| `premium-per` | +AI Thinking | 5–10 | Multi-page invoices, short contracts |
| `premium-per-max` | +AI Thinking | 20–50+ | Long contracts, reports |
| `ultra` | +AI Reasoning | 1–3 | Complex single documents, handwritten |
| `ultra-per` | +AI Reasoning | 5–10 | Complex multi-page contracts |
| `ultra-per-max` | +AI Reasoning | 20–50+ | **Legal documents, insurance policies, technical manuals** |

> **Important:** Using a model without sufficient page capacity for your document will only process the first N pages. Always use `-per` or `-per-max` variants for multi-page documents.

## Localized templates

| Collection | Output language | Optimized for |
|---|---|---|
| `invoice` | English | International invoices |
| `invoice:de` | German | German invoices, DATEV-compatible output |
| `invoice:en` | English | English invoices |
| `invoice:es` | Spanish | Spanish invoices |

## All available IDP collections (29)

The PaperOffice IDP engine supports these built-in extraction templates:

### Financial documents

| Collection | Document type |
|---|---|
| `invoice` | Invoices (international) |
| `invoice:de` | Invoices (German, DATEV-optimized) |
| `receipt` | Receipts and till slips |
| `cash_receipt` | Cash receipts |
| `hotel_invoice` | Hotel invoices |
| `accounting_datev` | DATEV SKR03 export |
| `statement_of_account` | Bank statements |
| `bank_check` | Bank checks |
| `bank_details` | Bank detail extraction |
| `payroll` | Payroll / pay stubs |
| `us_tax_forms` | US tax forms |

### Business documents

| Collection | Document type |
|---|---|
| `contract` | Contracts (all types) |
| `order` | Purchase orders |
| `delivery_note` | Delivery notes |
| `shipping_waybill` | Shipping waybills |
| `letter_mail` | Letters / mail |
| `utility_bill` | Utility bills |

### Identity & legal

| Collection | Document type |
|---|---|
| `identity_document` | ID cards, passports, driver's licenses |
| `vehicle_license` | Vehicle registrations |
| `legal_document` | Legal documents |
| `insurance_policy` | Insurance policies |
| `government_forms` | Government forms |

### Special types

| Collection | Document type |
|---|---|
| `handwritten_document` | Handwritten documents |
| `handwritten_customer_form` | Handwritten customer forms |
| `construction_plan` | Construction plans / blueprints |
| `variable_metadata` | Maximum metadata extraction |
| `idp_light` | Basic field extraction (fast, fewer fields) |
| `document_analysis` | General document analysis |

## How to run

```bash
export PAPEROFFICE_API_KEY="your_api_key"

# Bash
bash example.sh invoice.pdf

# Python
pip install requests
python3 example.py invoice.pdf

# Node.js
npm install form-data
node example.js invoice.pdf
```

## Available invoice fields

The IDP engine extracts the following fields (prefix `_`):

### Header data

| Field                    | Type     | Description                         |
|--------------------------|----------|-------------------------------------|
| `_invoice_number`        | string   | Invoice number                      |
| `_invoice_date`          | date     | Invoice date                        |
| `_invoice_due_date`      | date     | Due date                            |
| `_invoice_type`          | string   | Invoice type (invoice/credit note)  |
| `_invoice_description`   | string   | Description / subject               |
| `_purchase_order_number` | string   | Purchase order number               |
| `_delivery_date`         | date     | Delivery date                       |

### Amounts

| Field                    | Type     | Description                         |
|--------------------------|----------|-------------------------------------|
| `_total_amount`          | number   | Total amount (gross)                |
| `_net_amount`            | number   | Net amount                          |
| `_vat_amount`            | number   | VAT amount                          |
| `_vat_rate`              | number   | VAT rate in percent                 |
| `_discount_amount`       | number   | Discount amount                     |
| `_currency`              | string   | Currency (EUR, USD, etc.)           |

### Supplier (creditor)

| Field                    | Type     | Description                         |
|--------------------------|----------|-------------------------------------|
| `_supplier_name`         | string   | Supplier company name               |
| `_supplier_address`      | string   | Supplier address                    |
| `_supplier_vat_id`       | string   | Supplier VAT ID                     |
| `_supplier_tax_id`       | string   | Supplier tax number                 |
| `_supplier_email`        | string   | Supplier email                      |
| `_supplier_phone`        | string   | Supplier phone                      |

### Customer (debtor)

| Field                    | Type     | Description                         |
|--------------------------|----------|-------------------------------------|
| `_customer_name`         | string   | Customer company name               |
| `_customer_address`      | string   | Customer address                    |
| `_customer_vat_id`       | string   | Customer VAT ID                     |
| `_customer_number`       | string   | Customer number                     |

### Bank details

| Field                    | Type     | Description                         |
|--------------------------|----------|-------------------------------------|
| `_creditor_iban`         | string   | Creditor IBAN                       |
| `_creditor_bic`          | string   | Creditor BIC/SWIFT                  |
| `_creditor_bank_name`    | string   | Creditor bank name                  |
| `_payment_reference`     | string   | Payment reference                   |
| `_payment_terms`         | string   | Payment terms                       |

### Line items (table)

| Field                    | Type     | Description                         |
|--------------------------|----------|-------------------------------------|
| `_line_items`            | table    | Individual invoice line items       |

The `_line_items` table can contain per row: description, quantity, unit price, total price, VAT rate.

## Response structure

```json
{
  "status": "success",
  "job_id": "poai-job_900_...",
  "operation": "document_idp",
  "pipeline": "workflow",
  "result": {
    "pages_idp": [{
      "document_information": { "total_pages": 1 },
      "suggested_fields": {
        "_invoice_number": {
          "type": "string",
          "value": "2024-001",
          "value_raw": "2024-001",
          "source_boxes": [0],
          "source_boxes_confidence": "high"
        },
        "_total_amount": {
          "type": "number",
          "value": "1.469,06",
          "value_raw": "1469.06",
          "source_boxes_confidence": "high"
        }
      }
    }]
  }
}
```

## Field metadata & bounding boxes

Every extracted field contains metadata that traces exactly WHERE in the document the value was found:

| Property | Type | Description |
|---|---|---|
| `type` | string | Data type: `string`, `number`, `date`, `table` |
| `value` | string | Formatted value (e.g. `"1.469,06"`) |
| `value_raw` | string | Raw value for processing (e.g. `"1469.06"`) |
| `source_boxes` | array | **Bounding box IDs** referencing positions in the document |
| `source_boxes_confidence` | string | Extraction confidence: `high`, `medium`, `low` |

### How source_boxes work

The `source_boxes` array contains **integer IDs** that reference OCR bounding boxes on the page. Each ID maps to a text region with pixel coordinates (x, y, width, height):

```json
{
  "_invoice_number": {
    "type": "string",
    "value": "2024-001",
    "value_raw": "2024-001",
    "source_boxes": [0, 1],
    "source_boxes_confidence": "high"
  }
}
```

> `source_boxes: [0, 1]` means the invoice number was found in OCR bounding boxes #0 and #1. These IDs can be used for visual highlighting, validation UIs, or targeted redaction.

### Confidence levels

| Level | Meaning | Recommended action |
|---|---|---|
| `high` | AI is confident in the extraction | Use directly |
| `medium` | Likely correct, some uncertainty | Flag for review in critical workflows |
| `low` | Uncertain, may be incorrect | Manual review required |

## Tips

- Use **`value_raw`** for numerical processing (dot as decimal separator)
- When **`source_boxes_confidence`** is `"low"` → manual review recommended
- Use **`model=ultra`** for complex multi-page invoices with many line items
- Use `source_boxes` IDs for building validation UIs that highlight found values
