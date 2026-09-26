# Upload document (DMS Upload)

Uploads a document to the PaperOffice DMS. Documents are automatically indexed and immediately discoverable via **Smart Search**.

## Endpoint

```
POST https://api.paperoffice.ai/latest/documents/document-put
```

**Authentication:** Bearer Token (API key required)

## Parameters

| Parameter | Type | Required | Description |
|---|---|---|---|
| `file` | file | **Yes** | File to upload (multipart/form-data) — **not** `file_1`! |
| `workspace_id` | int | **Yes** | Target workspace ID |
| `workspace_name` | string | No | Workspace name (alternative to `workspace_id`) |

> **Important:** The file parameter is `file` (not `file_1`). The `workspace_id` is the numeric ID from the workspace-list endpoint.

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
  "workspace_id": 28,
  "workspace_name": "Workspace [SANDBOX] for xAI Grok",
  "ai_dms_refused_count": 0,
  "results": [
    {
      "status": "success",
      "filename": "contract.pdf",
      "documents_id": 1168,
      "pofid": "5a5b4f1b...POD1.AI256880.MT1790419691639.pdf",
      "workspace_id": 28,
      "size": 22692,
      "total_pages": 1,
      "version": 1,
      "ai_dms": { "mode": "ultra", "status": "queued" }
    }
  ]
}
```

`document-put` accepts one or more files; each file is reported in `results[]`. If the workspace has AI-DMS enabled, processing starts automatically and is charged according to the workspace mode.

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
