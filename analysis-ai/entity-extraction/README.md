# Entity Extraction — Entities of Processed Documents

Returns the named entities the AI-DMS extracted from a document: companies, persons, IBANs, amounts, dates, e-mail addresses, phone numbers, invoice and contract numbers. Entities are created when a document is processed (AI-DMS or an IDP workflow); this endpoint reads them.

## Endpoints

| Endpoint | Method | Purpose |
|---|---|---|
| `/document_intelligence/entities` | GET | Entities of one document (`documents_id`) |
| `/document_intelligence/entities/{pofid}` | GET | Same by POFID, optional `include_relations` |
| `/document_intelligence/entities/search` | GET | Search entities across all documents |
| `/document_intelligence/entities/canonical` | GET | Canonical (deduplicated) entities of the account |

**Authentication:** Bearer token

## Parameters — `GET /document_intelligence/entities`

| Parameter | Type | Required | Description |
|---|---|---|---|
| `documents_id` | int | Yes | Numeric document ID (from `POST /documents/document-search`) |
| `type` | string | No | Filter: `company`, `person`, `iban`, `amount`, `email`, `phone`, `location`, `invoice_number`, `contract_number` |
| `min_confidence` | float | No | Minimum confidence (0.0–1.0) |

## Parameters — `GET /document_intelligence/entities/search`

| Parameter | Type | Required | Description |
|---|---|---|---|
| `query` | string | Yes | Search term (company name, IBAN, person ...) |
| `workspace_id` | int | No | Restrict to a workspace |
| `entity_type` | string | No | Filter by type |
| `limit` | int | No | Max results |

## How to run

```bash
export PAPEROFFICE_API_KEY=po_ut_xxx

# documents_id: take it from POST /documents/document-search
bash example.sh 668
python3 example.py 668 company
node example.js 668
```

## Expected response

```json
{
  "status": "success",
  "document_id": 668,
  "pofid": "...",
  "file_name": "08_invoice_RE-2026-7834_scan.pdf",
  "total": 5,
  "entities": [
    {
      "type": "company",
      "type_label": "Firma",
      "value": "Northstar Industrial Systems Ltd.",
      "normalized_value": "northstar industrial systems ltd.",
      "confidence": 0.9,
      "page_number": null,
      "source": "entity_extraction"
    }
  ],
  "by_type": { "company": 2, "amount": 1, "date": 2 },
  "entity_types": ["company", "amount", "date"]
}
```

## Entity types

| Type | Examples |
|---|---|
| `company` | Northstar Industrial Systems Ltd. |
| `person` | John Smith |
| `iban` | DE89 3704 0044 0532 0130 00 |
| `amount` | 47500 EUR |
| `date` | 2026-03-15 |
| `email` | info@example.com |
| `phone` | +49 30 123456 |
| `invoice_number`, `contract_number` | RE-2026-7834 |

## Common use cases

- **Contract analysis:** Automatically extract parties, amounts and deadlines from contracts
- **Invoice processing:** Recognize suppliers, invoice numbers and totals
- **Compliance:** Identify personal data in documents (GDPR)
- **Knowledge management:** Extract entities for knowledge graph construction
