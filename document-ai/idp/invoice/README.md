# Invoice Extraction (IDP Invoice)

Extracts **28+ structured fields** from invoices — invoice number, amounts, supplier, IBAN, line items, and more. Each field includes confidence scores and bounding boxes.

## Endpoint

```
POST https://api.paperoffice.ai/latest/job/add/workflow
```

**Authentication:** Bearer Token (API key required)

## Parameters

| Parameter         | Value      | Description                          |
|-------------------|------------|--------------------------------------|
| `file_1`          | File       | PDF or image of the invoice          |
| `model`           | `premium`  | Extraction quality (basic/premium/ultra) |
| `idp_collection`  | `invoice`  | Enable invoice extraction            |
| `priority`        | `900`      | Synchronous processing (≥900)        |

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

## Field metadata

Each field contains:

| Property                  | Description                               |
|---------------------------|-------------------------------------------|
| `type`                    | Data type (string, number, date, table)   |
| `value`                   | Formatted value (e.g. "1.469,06")         |
| `value_raw`               | Raw value for further processing ("1469.06") |
| `source_boxes`            | Positions in the document (bounding boxes)|
| `source_boxes_confidence` | Confidence: high, medium, low             |

## Tips

- Use **`value_raw`** for numerical processing (dot as decimal separator)
- When **`source_boxes_confidence`** is "low" → manual review recommended
- Use **`model=ultra`** for complex multi-page invoices with many line items
