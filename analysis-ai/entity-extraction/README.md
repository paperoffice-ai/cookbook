# Entity Extraction — Named Entity Recognition (NER)

Extracts named entities (persons, organizations, locations, dates, amounts, etc.) from texts or documents using AI-powered NER analysis.

## Endpoints

| Endpoint | Method | Purpose |
|---|---|---|
| `/document_intelligence/entities` | POST | Extract entities from text |
| `/document_intelligence/entities/{document_id}` | GET | Get entities for an existing DMS document |
| `/document_intelligence/entities/search` | GET | Search entities across all documents |
| `/document_intelligence/entities/canonical` | GET | Get canonical (deduplicated) entities |

**Authentication:** Bearer Token

## Parameters — `POST /document_intelligence/entities`

| Parameter | Type | Required | Description |
|---|---|---|---|
| `text` | string | Yes | Text to analyze |
| `type` | string | No | Filter by entity type (e.g., `person`, `organization`, `location`) |
| `min_confidence` | float | No | Minimum confidence threshold (0.0–1.0) |
| `include_positions` | bool | No | Include character positions in the response |

## Parameters — `GET /document_intelligence/entities/{document_id}`

Returns entities extracted from an already-indexed DMS document.

| Parameter | Type | Required | Description |
|---|---|---|---|
| `{document_id}` | path | Yes | DMS document ID |
| `include_relations` | bool | No | Include entity relationships |

## Parameters — `GET /document_intelligence/entities/search`

| Parameter | Type | Required | Description |
|---|---|---|---|
| `query` | string | Yes | Search term |
| `workspace_id` | int | No | Restrict to a workspace |
| `entity_type` | string | No | Filter by type |
| `limit` | int | No | Max results |

## How to run

```bash
export PAPEROFFICE_API_KEY=po_sk_xxx

# Bash
bash example.sh "The company ABC GmbH is located in Berlin."

# Python
pip install requests
python3 example.py "The company ABC GmbH is located in Berlin."

# Node.js (v18+)
node example.js "The company ABC GmbH is located in Berlin."
```

## Expected response

```json
{
    "status": "success",
    "entities": [
        {
            "text": "Acme Corporation",
            "type": "organization",
            "start": 0,
            "end": 16,
            "confidence": 0.95
        },
        {
            "text": "New York",
            "type": "location",
            "start": 27,
            "end": 35,
            "confidence": 0.98
        },
        {
            "text": "March 15, 2025",
            "type": "date",
            "start": 82,
            "end": 96,
            "confidence": 0.97
        },
        {
            "text": "250,000 USD",
            "type": "money",
            "start": 62,
            "end": 73,
            "confidence": 0.96
        }
    ]
}
```

## Supported entity types

| Type | Description | Examples |
|---|---|---|
| `person` | Person names | John Smith, Dr. Miller |
| `organization` | Companies, authorities | Acme Corp., IRS |
| `location` | Places, addresses | New York, 5th Avenue |
| `date` | Date references | March 15, 2025, Q1/2024 |
| `money` | Monetary amounts | 250,000 USD, 1,500.00 EUR |
| `phone` | Phone numbers | +1 212 555 0123 |
| `email` | Email addresses | info@example.com |

## Common use cases

- **Contract analysis:** Automatically extract parties, amounts and deadlines from contracts
- **Invoice processing:** Recognize suppliers, invoice numbers and totals
- **Compliance:** Identify personal data in documents (GDPR)
- **Knowledge management:** Extract entities for knowledge graph construction
