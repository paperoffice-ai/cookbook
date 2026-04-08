# Knowledge Base — CRUD Operations

Create, read, update and delete knowledge bases and their articles. A knowledge base is a structured knowledge container that organizes articles and makes them available for semantic search.

## Endpoints

```
GET  https://api.paperoffice.ai/latest/knowledge/kb_list
POST https://api.paperoffice.ai/latest/knowledge/kb_create
POST https://api.paperoffice.ai/latest/knowledge/kb_update
POST https://api.paperoffice.ai/latest/knowledge/kb_delete

POST https://api.paperoffice.ai/latest/knowledge/article_create
GET  https://api.paperoffice.ai/latest/knowledge/article_list
POST https://api.paperoffice.ai/latest/knowledge/article_update
POST https://api.paperoffice.ai/latest/knowledge/article_delete
```

**Authentication:** Bearer Token for all endpoints.

## Parameters

### Knowledge Base

| Endpoint | Parameter | Type | Required | Description |
|---|---|---|---|---|
| `kb_create` | `name` | string | ✅ | Name of the knowledge base |
| | `description` | string | ❌ | Description |
| | `visibility` | string | ❌ | Visibility |
| | `primary_language` | string | ❌ | Language (e.g. `de`, `en`) |
| `kb_update` | `kb_id` | int | ✅ | ID of the KB |
| | `name` | string | ❌ | New name |
| | `description` | string | ❌ | New description |
| `kb_delete` | `kb_id` | int | ✅ | ID of the KB to delete |

### Articles

| Endpoint | Parameter | Type | Required | Description |
|---|---|---|---|---|
| `article_create` | `kb_id` | int | ✅ | ID of the target KB |
| | `title` | string | ✅ | Article title |
| | `content` | string | ✅ | Content |
| | `category` | string | ❌ | Category |
| `article_list` | `kb_id` | int | ✅ | KB ID (query parameter) |
| `article_update` | `article_id` | int | ✅ | ID of the article |
| | `title` | string | ❌ | New title |
| | `content` | string | ❌ | New content |
| `article_delete` | `article_id` | int | ✅ | ID of the article to delete |

## How to Run

```bash
export PAPEROFFICE_API_KEY=po_sk_xxx

# Bash — Create KB, add articles, list, cleanup
bash example.sh

# Python — Complete CRUD cycle with all operations
pip install requests
python3 example.py

# Node.js (v18+) — CRUD with async/await
node example.js
```

## Expected Response (kb_list)

```json
{
    "status": "success",
    "count": 1,
    "data": [
        {
            "id": 9,
            "slug": "qa-kb-april6",
            "name": "QA-KB-April6",
            "status": "active"
        }
    ]
}
```

## Workflow

1. **Create KB** → `kb_create` returns the new KB with ID
2. **Add articles** → `article_create` with `kb_id` as reference
3. **Search articles** → See recipe `kb-search/`
4. **Update** → `kb_update` / `article_update` with respective ID
5. **Delete** → `kb_delete` removes KB including all articles

## Use Cases

- **Helpdesk:** Create FAQ articles and make them searchable for AI agents
- **Onboarding:** Build a knowledge base with training material
- **Product documentation:** Centrally manage API references and guides
- **Internal wiki:** Store and maintain departmental knowledge in a structured way
