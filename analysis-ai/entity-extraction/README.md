# Entity Extraction — Named Entity Recognition (NER)

Extracts named entities (persons, organizations, locations, dates, amounts, etc.) from texts or documents using AI-powered NER analysis.

## Endpoint

```
POST https://api.paperoffice.ai/latest/document_intelligence/entities
```

**Authentication:** Bearer Token

## Parameters

| Parameter | Type | Required | Description |
|---|---|---|---|
| `text` | string | ✅* | Text to analyze |
| `file_1` | file | ✅* | Alternatively: upload a document (PDF, DOCX, etc.) |
| `entity_types` | string | ❌ | Comma-separated list: `person`, `organization`, `location`, `date`, `money`, `phone`, `email` |

\* Either `text` or `file_1` must be provided.

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
