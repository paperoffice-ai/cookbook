# AI-Powered Document Generation — Complete Reference

Create documents from **content (Markdown/HTML)** or from **templates with variables**. Generated documents are automatically stored in the DMS.

## Endpoints

| Endpoint | Method | Description |
|---|---|---|
| `/document_generation/create-from-content` | POST | Generate PDF from Markdown or HTML content |
| `/document_generation/create-from-template` | POST | Generate PDF from template with variables |
| `/document_generation/template-create` | POST | Create a reusable document template |

**Authentication:** Bearer Token (API key required)

---

## 1. Create from content

Generate a PDF from Markdown or HTML content, stored directly in a DMS workspace.

```
POST https://api.paperoffice.ai/latest/document_generation/create-from-content
```

### Parameters

| Parameter | Type | Required | Default | Description |
|---|---|---|---|---|
| `content` | string | **Yes** | — | Markdown or HTML content for the document |
| `content_type` | string | No | `markdown` | `markdown` or `html` |
| `output_format` | string | No | `pdf` | Output format (currently `pdf`) |
| `title` | string | No | — | Document title (also used as filename) |
| `workspace_id` | int | **Yes** | — | Target workspace ID (use `po_Workspaces_list` to find valid IDs) |
| `metadata` | object | No | — | Key-value pairs stored as IDP fields |
| `language` | string | No | `de` | Language for formatting (`de`, `en`) |
| `auto_classify` | bool | No | — | Automatically classify the document on creation |
| `custom_css` | string | No | — | Additional CSS for PDF layout |
| `header_html` | string | No | — | HTML for page header |
| `footer_html` | string | No | — | HTML for page footer |

### Example — Markdown to PDF

```bash
curl -X POST "https://api.paperoffice.ai/latest/document_generation/create-from-content" \
  -H "Authorization: Bearer $PAPEROFFICE_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "content": "# Monthly Report\n\n## Summary\n\nRevenue increased by **12%** compared to Q1...",
    "content_type": "markdown",
    "title": "Monthly Report April 2026",
    "workspace_id": 123,
    "language": "en",
    "custom_css": "body { font-family: Arial; } h1 { color: #003366; }",
    "footer_html": "<div style=\"text-align: center; font-size: 10px;\">Confidential — Page {{page}}</div>"
  }'
```

---

## 2. Create from template

Generate a PDF by filling template placeholders with data.

```
POST https://api.paperoffice.ai/latest/document_generation/create-from-template
```

### Parameters

| Parameter | Type | Required | Default | Description |
|---|---|---|---|---|
| `template_id` | string | **Yes** | — | Template ID (e.g., `tpl_invoice_standard`) |
| `variables` | object | **Yes** | — | Variable values for the placeholders. Use arrays for `{{#each}}` blocks |
| `output_format` | string | No | `pdf` | Currently `pdf` |
| `workspace_id` | int | **Yes** | — | Target workspace ID |
| `title` | string | No | — | Document title (overrides template name). May contain `{{variable}}` placeholders |
| `metadata` | object | No | — | Additional metadata |
| `auto_classify` | bool | No | — | Auto-classify on creation |

### Example — Invoice from template

```bash
curl -X POST "https://api.paperoffice.ai/latest/document_generation/create-from-template" \
  -H "Authorization: Bearer $PAPEROFFICE_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "template_id": "tpl_invoice_standard",
    "variables": {
      "company": "Acme Corporation",
      "invoice_number": "2026-042",
      "amount": "1,250.00",
      "date": "2026-04-08",
      "items": [
        { "description": "Consulting", "hours": 8, "rate": 150 },
        { "description": "Development", "hours": 16, "rate": 120 }
      ]
    },
    "workspace_id": 123,
    "title": "Invoice {{invoice_number}} — {{company}}"
  }'
```

---

## 3. Create template

Create a reusable HTML template with placeholders.

```
POST https://api.paperoffice.ai/latest/document_generation/template-create
```

### Parameters

| Parameter | Type | Required | Default | Description |
|---|---|---|---|---|
| `name` | string | **Yes** | — | Template name |
| `html_content` | string | **Yes** | — | HTML with `{{variable}}` placeholders |
| `template_id` | string | No | auto-generated | Unique template ID |
| `description` | string | No | — | Template description |
| `category` | string | No | `general` | Category: `invoices`, `contracts`, `reports`, `general` |
| `variables_schema` | object | No | — | JSON Schema for expected variables |
| `page_format` | string | No | `A4` | `A4`, `A3`, `Letter` |
| `page_orientation` | string | No | `portrait` | `portrait` or `landscape` |
| `margin_top` | int | No | `20` | Top margin (mm) |
| `margin_right` | int | No | `15` | Right margin (mm) |
| `margin_bottom` | int | No | `20` | Bottom margin (mm) |
| `margin_left` | int | No | `15` | Left margin (mm) |
| `header_html` | string | No | — | HTML for page header |
| `footer_html` | string | No | — | HTML for page footer |

### Template syntax

Templates use Handlebars-style placeholders:

| Syntax | Description | Example |
|---|---|---|
| `{{variable}}` | Simple replacement | `{{company_name}}` |
| `{{#each items}}...{{/each}}` | Loop over arrays | Line items in invoices |
| `{{#if condition}}...{{/if}}` | Conditional blocks | Optional sections |

### Example — Create invoice template

```bash
curl -X POST "https://api.paperoffice.ai/latest/document_generation/template-create" \
  -H "Authorization: Bearer $PAPEROFFICE_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Standard Invoice",
    "template_id": "tpl_invoice_standard",
    "category": "invoices",
    "page_format": "A4",
    "page_orientation": "portrait",
    "margin_top": 25,
    "margin_bottom": 25,
    "html_content": "<h1>Invoice {{invoice_number}}</h1><p>To: {{company}}</p><table><tr><th>Item</th><th>Amount</th></tr>{{#each items}}<tr><td>{{description}}</td><td>{{amount}} EUR</td></tr>{{/each}}</table>",
    "footer_html": "<div style=\"text-align: center;\">Page {{page}} of {{pages}}</div>"
  }'
```

---

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
  "document_id": 1164,
  "pofid": "5ce2a929...POD3.AI256880.MT1790419639444.pdf",
  "file_name": "Cookbook smoke doc.pdf",
  "format": "pdf",
  "mime_type": "application/pdf",
  "file_size": 43034,
  "charged_this_request": 10,
  "idempotent_replay": false,
  "ai_dms": { "mode": "ultra", "status": "queued" }
}
```

The PDF is stored in the workspace. Download it with `GET /documents/document-download/{pofid}`. Send an `idempotency_key` (8–128 characters): the same key with the same payload replays the stored document at no charge; the same key with a changed payload is rejected with `IDEMPOTENCY_CONFLICT`.

## Workflow: Template → Document → DMS

```
1. Create template (once)     → template-create
2. Fill variables              → create-from-template
3. Document saved to DMS       → auto-stored in workspace_id
4. Search & retrieve           → smart-search or document-chat
```

## Tips

- `custom_css` supports full CSS — use it for fonts, colors, spacing
- `header_html` / `footer_html` support `{{page}}` and `{{pages}}` placeholders
- Generated documents are automatically indexed for DMS search
- Use `auto_classify=true` to automatically detect document type
- Download URLs are time-limited — download immediately after generation
