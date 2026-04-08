# Create & Manage Workspaces — Complete Reference

Workspaces are the top-level organizational unit in the PaperOffice DMS. Each workspace forms an **isolated document area** with its own permissions, search indexes, and security settings.

## Endpoints

| Action | Method | Path |
|---|---|---|
| Create | POST | `/documents/workspace-create` |
| List | GET | `/documents/workspace-list` |

**Authentication:** Bearer Token (API key required)

## Parameters (Create)

### Required

| Parameter | Type | Required | Description |
|---|---|---|---|
| `name` | string | **Yes** | Name of the workspace (must not be empty) |

### Security & compliance

| Parameter | Type | Default | Description |
|---|---|---|---|
| `workspace_tier` | string | `standard` | Security level: `standard`, `confidential`, `compliance` (highest) |
| `is_revision_secure` | bool | `false` | Enable WORM protection (write-once, read-many). **Irreversible once enabled!** Requires PaperOffice EU Cloud |
| `retention_years` | int | `10` | Document retention period in years (1–99). Default: 10 (GoBD-compliant) |
| `workspace_password` | string | — | Password-protect workspace access |

### AI processing

| Parameter | Type | Default | Description |
|---|---|---|---|
| `ai_dms_mode` | string | `disabled` | AI processing mode: `disabled`, `basic`, `premium`, `ultra` |

When set to `basic`/`premium`/`ultra`, uploaded documents are automatically:
- OCR-processed (text extraction)
- Classified (document type detection)
- Field-extracted (IDP)
- Indexed for semantic search

### Storage

| Parameter | Type | Default | Description |
|---|---|---|---|
| `storage_mode` | string | `cloud` | `cloud` (PaperOffice EU Cloud) or `byos` (Bring Your Own Storage). **Cannot be changed after creation** |
| `storage_mount_id` | int | — | Storage mount ID (for BYOS mode) |
| `storage_mount_path` | string | — | Path on the storage mount (for BYOS mode) |

### Organization

| Parameter | Type | Default | Description |
|---|---|---|---|
| `description` | string | — | Workspace description |
| `type` | string | `folder` | Workspace type |
| `default_locale` | string | — | Default language/region (`de:DE`, `en:US`, etc.) |
| `priority` | int | `500` | Sort priority |
| `is_default` | bool | — | Mark as default workspace |
| `is_stealth` | bool | — | Hide workspace (stealth mode) |
| `is_archived` | bool | — | Archive workspace |
| `color` | string | — | Color code for UI |
| `icon` | string | — | Icon for UI |
| `image` | string | — | Image URL |
| `tags` | array | — | Tags for categorization |

### Contact information

| Parameter | Type | Description |
|---|---|---|
| `contact_salutation` | string | Contact salutation |
| `contact_firstname` | string | Contact first name |
| `contact_lastname` | string | Contact last name |
| `contact_email` | string | Contact email |
| `contact_phone` | string | Contact phone |
| `company_name` | string | Company name |
| `address_street` | string | Street address |
| `address_zip` | string | Postal code |
| `address_city` | string | City |
| `address_country` | string | Country |

### Custom metadata

| Parameter | Type | Description |
|---|---|---|
| `metadata` | object | Additional metadata as JSON object |

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

## Example — Create compliance workspace

```bash
curl -X POST "https://api.paperoffice.ai/latest/documents/workspace-create" \
  -H "Authorization: Bearer $PAPEROFFICE_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Finance Archive 2026",
    "description": "GoBD-compliant financial document archive",
    "workspace_tier": "compliance",
    "is_revision_secure": true,
    "retention_years": 10,
    "ai_dms_mode": "premium",
    "storage_mode": "cloud",
    "default_locale": "en:US",
    "company_name": "Acme Corporation",
    "tags": ["finance", "archive", "2026"]
  }'
```

## Response structure (Create)

```json
{
  "status": "success",
  "workspace": {
    "id": 42,
    "name": "Finance Archive 2026",
    "description": "GoBD-compliant financial document archive",
    "workspace_tier": "compliance",
    "is_revision_secure": true,
    "ai_dms_mode": "premium",
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
      "name": "Finance Archive 2026",
      "description": "GoBD-compliant financial document archive",
      "workspace_tier": "compliance",
      "ai_dms_mode": "premium"
    }
  ]
}
```

## Workspace tiers

| Tier | Security level | Features |
|---|---|---|
| `standard` | Normal | Basic document storage, search, sharing |
| `confidential` | High | Encrypted storage, access logging, restricted sharing |
| `compliance` | Highest | WORM protection, audit trail, retention enforcement, GoBD/GDPR-compliant |

## AI-DMS modes

| Mode | Description | Auto-features |
|---|---|---|
| `disabled` | No AI processing | Manual only |
| `basic` | OCR + Vision | Text extraction, basic classification |
| `premium` | + AI Thinking | Full IDP, semantic indexing, smart classification |
| `ultra` | + AI Reasoning | Complex documents, handwritten, multi-language |

## Storage modes

| Mode | Description |
|---|---|
| `cloud` | PaperOffice EU Cloud (default) — GDPR-compliant, managed storage |
| `byos` | Bring Your Own Storage — connect your own S3, NAS, or cloud storage |

> **Important:** Storage mode cannot be changed after workspace creation!

## Tips

- Workspace names should be unique and descriptive
- Create one workspace per department, project, or compliance requirement
- Use `workspace_tier=compliance` + `is_revision_secure=true` for audit-proof archives
- Enable `ai_dms_mode` for automatic document processing on upload
- WORM protection (`is_revision_secure`) is **irreversible** — documents cannot be deleted or modified

## See also

- [Document Upload](../document-upload/) — Upload documents to a workspace
- [Smart Search](../smart-search/) — Search across workspaces
- [Document Chat](../document-chat/) — Chat with documents
