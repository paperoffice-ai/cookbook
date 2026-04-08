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
            "text": "Mustermann GmbH",
            "type": "organization",
            "start": 4,
            "end": 19,
            "confidence": 0.95
        },
        {
            "text": "München",
            "type": "location",
            "start": 33,
            "end": 40,
            "confidence": 0.98
        },
        {
            "text": "15. März 2025",
            "type": "date",
            "start": 48,
            "end": 61,
            "confidence": 0.97
        },
        {
            "text": "250.000 EUR",
            "type": "money",
            "start": 83,
            "end": 94,
            "confidence": 0.96
        }
    ]
}
```

## Supported entity types

| Type | Description | Examples |
|---|---|---|
| `person` | Person names | Max Mustermann, Dr. Meier |
| `organization` | Companies, authorities | Mustermann GmbH, Finanzamt München |
| `location` | Places, addresses | München, Hauptstraße 5 |
| `date` | Date references | 15. März 2025, Q1/2024 |
| `money` | Monetary amounts | 250.000 EUR, 1.500,00 € |
| `phone` | Phone numbers | +49 89 123456 |
| `email` | Email addresses | info@beispiel.de |

## Common use cases

- **Contract analysis:** Automatically extract parties, amounts and deadlines from contracts
- **Invoice processing:** Recognize suppliers, invoice numbers and totals
- **Compliance:** Identify personal data in documents (GDPR)
- **Knowledge management:** Extract entities for knowledge graph construction
