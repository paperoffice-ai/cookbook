# AI-powered document generation (Document Generation)

Creates documents from **templates with variables** — invoices, contracts, reports and more. The AI fills placeholders automatically and generates formatted PDF or DOCX files.

## Endpoint

```
POST https://api.paperoffice.ai/latest/document_generation/generate
```

**Authentication:** Bearer Token (API key required)

## Parameters

| Parameter       | Required | Description                                     |
|-----------------|----------|-------------------------------------------------|
| `template`      | Yes      | Name of the template (e.g. "invoice_standard")  |
| `variables`     | No       | JSON object with template variables              |
| `output_format` | No       | Output format: `pdf` (default) or `docx`         |

## How to run

```bash
export PAPEROFFICE_API_KEY="your_api_key"

# Bash
bash example.sh "invoice_standard" pdf

# Python
pip install requests
python3 example.py "invoice_standard" pdf

# Node.js
node example.js "invoice_standard" pdf
```

## Response structure

```json
{
  "status": "success",
  "document": {
    "download_url": "https://api.paperoffice.ai/latest/documents/download/abc123",
    "format": "pdf",
    "pages": 2
  }
}
```

## Template system

Templates use placeholders in the format `{{variable}}`:

```
Dear Sir or Madam,

we hereby invoice you for our services the following amount:

Invoice number: {{rechnungsnummer}}
Date:           {{datum}}
Company:        {{firma}}
Amount:         {{betrag}} EUR
```

## Variables

Variables are passed as a JSON object:

```json
{
  "firma": "Muster GmbH",
  "rechnungsnummer": "2026-042",
  "betrag": "1.250,00",
  "datum": "08.04.2026"
}
```

## Output formats

| Format | Description                                 |
|--------|---------------------------------------------|
| `pdf`  | PDF file (default) — ideal for sending      |
| `docx` | Word document — ideal for post-editing      |

## Tips

- **Define templates in advance** — reusable templates for frequently created documents
- **Validate variables** — missing placeholders will be left empty
- **Download URL** is time-limited — download immediately after generation
- Can be combined with `document-upload/` to archive generated documents in the DMS
