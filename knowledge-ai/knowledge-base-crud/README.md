# Knowledge Base — CRUD Operations (Complete Reference)

Create, read, update and delete knowledge bases and their articles. A knowledge base is a structured knowledge container that organizes articles and makes them available for semantic search.

## Endpoints

```
GET  https://api.paperoffice.ai/latest/knowledge/kb_list
POST https://api.paperoffice.ai/latest/knowledge/kb_add
POST https://api.paperoffice.ai/latest/knowledge/kb_update
POST https://api.paperoffice.ai/latest/knowledge/kb_delete

POST https://api.paperoffice.ai/latest/knowledge/add
GET  https://api.paperoffice.ai/latest/knowledge/list
GET  https://api.paperoffice.ai/latest/knowledge/get
POST https://api.paperoffice.ai/latest/knowledge/update
POST https://api.paperoffice.ai/latest/knowledge/delete
```

**Authentication:** Bearer Token for all endpoints.

## Knowledge Base parameters

### `kb_add`

| Parameter | Type | Required | Default | Description |
|---|---|---|---|---|
| `name` | string | **Yes** | — | Name of the knowledge base |
| `description` | string | No | — | Description |
| `slug` | string | No | auto-generated | URL-friendly slug |
| `visibility` | string | No | — | `public`, `private`, `internal` |
| `primary_language` | string | No | `de` | Primary language (`de`, `en`, `es`, `fr`, `it`, `pt`) |
| `enabled_languages` | bool | No | — | Enable multilingual support |
| `language` | string | No | — | Shorthand language code |
| `theme_color` | string | No | — | Hex color for branding (e.g., `#0066FF`) |
| `logo_url` | string | No | — | Logo URL |
| `settings` | object | No | — | Additional settings object |

### `kb_update`

| Parameter | Type | Required | Default | Description |
|---|---|---|---|---|
| `id` | int | **Yes** | — | ID of the KB to update |
| `name` | string | No | — | New name |
| `slug` | string | **Yes** | — | URL slug |
| `description` | string | **Yes** | — | Description |
| `visibility` | string | **Yes** | — | `public`, `private`, `internal` |
| `primary_language` | string | **Yes** | — | Primary language |
| `enabled_languages` | bool | **Yes** | — | Multilingual toggle |
| `theme_color` | string | **Yes** | — | Hex color |
| `logo_url` | string | **Yes** | — | Logo URL |
| `settings` | object | **Yes** | — | Settings object |

### `kb_delete`

| Parameter | Type | Required | Description |
|---|---|---|---|
| `id` | int | **Yes** | ID of the KB to delete |
| `hard` | bool | No | `true` = permanent delete, `false` = soft delete (default) |

## Article parameters

### `add` (create article)

| Parameter | Type | Required | Default | Description |
|---|---|---|---|---|
| `kb_id` | int | **Yes** | — | ID of the target knowledge base |
| `title` | string | **Yes** | — | Article title |
| `content` | string | **Yes** | — | Content (simple string or multilingual JSON object) |
| `type` | string | No | `article` | `article`, `faq`, `guide` |
| `category` | string | No | — | Category slug or name |
| `category_id` | int | No | — | Category ID (alternative to slug) |
| `language` | string | No | `de` | Language code — only used if `content` is a plain string |
| `selected_languages` | array | No | — | Target languages for auto-translation |
| `priority` | int | No | — | Priority for ordering |
| `position` | int | No | — | Position within category |
| `is_active` | bool | No | `true` | Active status (inactive articles are hidden from search) |
| `image_url` | string | No | — | Image URL for the article |

#### Multilingual content

The `content` parameter accepts two formats:

**Simple string** (auto-wrapped into the specified `language`):
```json
{
  "content": "This is the article content.",
  "language": "en"
}
```

**Multilingual JSON object** (explicit per-language):
```json
{
  "content": {
    "en": { "title": "How to reset password", "body": "Go to Settings..." },
    "de": { "title": "Passwort zurücksetzen", "body": "Gehe zu Einstellungen..." }
  }
}
```

### `update` (update article)

| Parameter | Type | Required | Description |
|---|---|---|---|
| `id` | int | **Yes** | ID of the article to update |
| `title` | string | No | New title |
| `content` | string | No | New content (string or multilingual JSON) |
| `knowledge_id` | int | No | Move to different KB |
| `type` | string | No | `article`, `faq`, `guide` |
| `category` | string | No | Category slug |
| `category_id` | int | No | Category ID |
| `image_url` | string | No | Image URL |
| `is_active` | bool | No | Active status |
| `priority` | int | No | Priority |
| `position` | int | No | Position |
| `selected_languages` | array | No | Target languages |

### `delete` (delete article)

| Parameter | Type | Required | Description |
|---|---|---|---|
| `id` | int | **Yes** | ID of the article to delete |
| `knowledge_id` | int | No | KB ID (for validation) |

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

1. **Create KB** → `kb_add` returns the new KB with ID
2. **Add articles** → `add` with `kb_id`, set `type` and `category`
3. **Search articles** → See recipe [KB Search](../kb-search/)
4. **Update** → `kb_update` / `update` with respective ID
5. **Delete** → `kb_delete` removes KB including all articles (`hard=true` for permanent)

## Use Cases

- **Helpdesk:** Create FAQ articles (`type=faq`) and make them searchable for AI agents
- **Onboarding:** Build a knowledge base with training guides (`type=guide`)
- **Product documentation:** Centrally manage API references and guides
- **Internal wiki:** Store and maintain departmental knowledge with categories
- **Multilingual support:** Create articles in multiple languages simultaneously
