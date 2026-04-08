# Create & manage workspaces

Workspaces are the top-level organizational unit in the PaperOffice DMS. Each workspace forms an **isolated document area** with its own permissions and search indexes.

## Endpoints

| Action | Method | Path                                |
|--------|--------|-------------------------------------|
| Create | POST   | `/documents/workspace_create`       |
| List   | GET    | `/documents/workspace_list`         |

**Authentication:** Bearer Token (API key required)

## Parameters (Create)

| Parameter     | Required | Description                         |
|---------------|----------|-------------------------------------|
| `name`        | Yes      | Name of the workspace               |
| `description` | No       | Optional description                |

## How to run

```bash
export PAPEROFFICE_API_KEY="your_api_key"

# Bash
bash example.sh "Accounting" "Invoices and receipts"

# Python
pip install requests
python3 example.py "Accounting" "Invoices and receipts"

# Node.js
node example.js "Accounting" "Invoices and receipts"
```

## Response structure (Create)

```json
{
  "status": "success",
  "workspace": {
    "id": 42,
    "name": "Accounting",
    "description": "Invoices and receipts",
    "created_at": "2026-04-08T10:30:00Z"
  }
}
```

## Response structure (List)

```json
{
  "status": "success",
  "workspaces": [
    {
      "id": 42,
      "name": "Accounting",
      "description": "Invoices and receipts"
    }
  ]
}
```

## Workspace concept

- **Isolation**: Documents in a workspace are only searchable within that workspace
- **Permissions**: Access is controlled per workspace via API keys
- **Tagging**: Within a workspace, documents can be further organized with tags
- **Search**: Each workspace has its own search index for fast queries

## Tips

- Workspace names should be unique and descriptive
- Create one workspace per department or project
- Regularly review the workspace list to check if all workspaces are still needed
