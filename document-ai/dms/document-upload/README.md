# Upload document (DMS Upload)

Uploads a document to the PaperOffice DMS. Documents are automatically indexed and immediately discoverable via **Smart Search**.

## Endpoint

```
POST https://api.paperoffice.ai/latest/documents/upload
```

**Authentication:** Bearer Token (API key required)

## Parameters

| Parameter        | Required | Description                                     |
|------------------|----------|-------------------------------------------------|
| `file_1`         | Yes      | File (PDF, DOCX, image, etc.)                   |
| `workspace_name` | Yes      | Target workspace for the document                |
| `tags`           | No       | Comma-separated tags (e.g. "invoice,2026,q1")   |
| `description`    | No       | Optional description of the document             |

## How to run

```bash
export PAPEROFFICE_API_KEY="your_api_key"

# Bash
bash example.sh contract.pdf "Accounting" "contract,2026"

# Python
pip install requests
python3 example.py contract.pdf "Accounting" "contract,2026"

# Node.js
npm install form-data
node example.js contract.pdf "Accounting" "contract,2026"
```

## Response structure

```json
{
  "status": "success",
  "document": {
    "id": 1234,
    "filename": "contract.pdf",
    "workspace": "Accounting",
    "tags": ["contract", "2026"],
    "size": 245760,
    "created_at": "2026-04-08T10:30:00Z"
  }
}
```

## Upload workflow

1. **Choose workspace** — Assign the document to an existing workspace
2. **Assign tags** — Comma-separated tags for later filtering
3. **Upload** — File is uploaded and automatically indexed
4. **Search** — Document is immediately discoverable via Smart Search

## Tagging strategy

Recommended tag categories:

| Category      | Examples                           |
|---------------|------------------------------------|
| Document type | `invoice`, `contract`, `quote`     |
| Time period   | `2026`, `q1`, `january`            |
| Department    | `accounting`, `hr`, `procurement`  |
| Status        | `open`, `reviewed`, `archived`     |
| Priority      | `important`, `urgent`              |

## Supported file formats

PDF, DOCX, DOC, XLSX, XLS, PPTX, PPT, TXT, CSV, PNG, JPG, TIFF, BMP, GIF, WEBP

## Tips

- **Create workspace first** — see recipe `workspace-setup/`
- **Use tags consistently** — greatly simplifies later searches
- **File size**: Maximum 50 MB per file
- After upload, the document can be queried immediately with `document-chat/`
