# DATEV Export from Invoice IDP

Extracts invoice data via IDP and automatically converts it into a **DATEV-compatible accounting entry** (CSV format for DATEV Unternehmen Online / Kanzlei-Rechnungswesen).

## Workflow

```
PDF invoice → PaperOffice IDP (invoice) → DATEV posting batch (CSV)
```

## Endpoint

```
POST https://api.paperoffice.ai/latest/job/add/workflow
```

**Authentication:** Bearer Token (API key required)

## Parameters

| Parameter | Type | Required | Default | Description |
|---|---|---|---|---|
| `file_1` | file | **Yes** | — | PDF of the invoice |
| `model` | string | **Yes** | — | 9 variants: `basic`, `premium`, `ultra` + `-per`/`-per-max` for more pages (see [Model tiers](../invoice/#model-tiers-9-variants)) |
| `idp_collection` | string | No | — | Must be `invoice` (or `invoice:de` for German output) |
| `idp_fields` | string | No | — | Additional custom fields as JSON |
| `priority` | int | No | `900` | `≥ 900` = synchronous (result inline) |

## How to run

```bash
export PAPEROFFICE_API_KEY="your_api_key"

# Bash — outputs DATEV CSV to stdout
bash example.sh invoice.pdf

# Python — with formatted output + CSV
python3 example.py invoice.pdf

# Python — write directly to CSV file
python3 example.py invoice.pdf > booking.csv

# Node.js
npm install form-data
node example.js invoice.pdf
```

## DATEV posting batch format

The generated CSV follows the **DATEV posting batch** format:

| Column                           | Example          | Source (IDP field)         |
|----------------------------------|------------------|----------------------------|
| Umsatz (ohne Soll/Haben-Kz)     | `1469.06`        | `_total_amount.value_raw`  |
| Soll/Haben-Kennzeichen           | `S`              | Fixed: debit               |
| Konto                            | `70000`          | Creditor (customizable)    |
| Gegenkonto                       | `1200`           | Bank (customizable)        |
| BU-Schlüssel                     | `9`              | Derived from `_vat_rate`   |
| Belegdatum                       | `1503`           | `_invoice_date` → DDMM    |
| Belegfeld 1                      | `2024-001`       | `_invoice_number`          |
| Buchungstext                     | `Acme Corp.`     | `_supplier_name`           |

### BU key mapping

| VAT rate | BU key      | Meaning                      |
|----------|-------------|------------------------------|
| 19%      | `9`         | Input tax 19%                |
| 7%       | `8`         | Input tax 7%                 |
| Other    | (empty)     | Assign manually              |

### Chart of accounts

The examples use **SKR04** as default:

| Account | Meaning                           |
|---------|-----------------------------------|
| 70000   | Creditor (collective account)     |
| 1200    | Bank                              |

For **SKR03**, adjust the account numbers in the examples (e.g. account `1800` for bank).

## Example output

```
--- Extracted Invoice Data ---
  Invoice no.:  2024-001
  Date:         2024-03-15
  Supplier:     Acme Corp.
  Amount:       1.469,06
  Net:          1.234,50
  VAT:          234,56

--- DATEV Accounting Entry (CSV) ---
Umsatz (ohne Soll/Haben-Kz);Soll/Haben-Kennzeichen;Konto;Gegenkonto;BU-Schlüssel;Belegdatum;Belegfeld 1;Buchungstext
1469.06;S;70000;1200;9;1503;2024-001;Acme Corp.
```

## Extension possibilities

- **Batch processing**: Loop over multiple PDFs → one consolidated posting batch
- **Account mapping**: Resolve supplier name → creditor account from master data
- **Validation**: Verify IBAN/VAT ID against PaperOffice validation APIs
- **DATEV XML**: Use DATEV XML format instead of CSV for more complex scenarios

## Field metadata & bounding boxes

The underlying IDP extraction provides traceability for every field:

| Property | Type | Description |
|---|---|---|
| `source_boxes` | array | Bounding box IDs showing WHERE in the invoice the value was found |
| `source_boxes_confidence` | string | Extraction confidence: `high`, `medium`, `low` |

> Use `source_boxes_confidence` to flag low-confidence amounts for manual review before importing into DATEV.

## Tips

- Use **`value_raw`** for amounts (dot as decimal separator, DATEV-compliant)
- DATEV expects the document date in **DDMM** format (without year, as defined in the header)
- For credit notes, set `Soll/Haben-Kennzeichen` to `H`
- When `source_boxes_confidence` is `"low"` for amount fields → always review before booking
