# Smart document search (Smart Search)

Searches the DMS with **semantic AI search**. Smart Search understands meaning and context — not just exact keywords.

## Endpoint

```
POST https://api.paperoffice.ai/latest/documents/search
```

**Authentication:** Bearer Token (API key required)

## Parameters

| Parameter        | Required | Description                                         |
|------------------|----------|-----------------------------------------------------|
| `global_search`  | Yes      | Search term (semantic + full-text)                   |
| `workspace_name` | No       | Restrict search to a specific workspace              |
| `limit`          | No       | Maximum number of results (default: 10)              |
| `offset`         | No       | Results starting from position (for pagination)      |

**Important:** The search parameter is called `global_search` (not `search_query`).

## How to run

```bash
export PAPEROFFICE_API_KEY="your_api_key"

# Bash
bash example.sh "contract terms"
bash example.sh "invoice 2026" "Accounting" 5

# Python
pip install requests
python3 example.py "contract terms"
python3 example.py "invoice 2026" "Accounting"

# Node.js
node example.js "contract terms"
node example.js "invoice 2026" "Accounting" 5
```

## Response structure

```json
{
  "status": "success",
  "results": [
    {
      "id": 1234,
      "filename": "framework_agreement_2026.pdf",
      "score": 0.94,
      "snippet": "The contract terms provide for a duration of...",
      "workspace": "Accounting"
    }
  ],
  "total": 42
}
```

## Search syntax

Smart Search supports different search modes:

| Mode              | Example                              | Description                        |
|-------------------|--------------------------------------|------------------------------------|
| Semantic search   | "termination clauses in lease"       | Finds contextually matching parts  |
| Keyword search    | "IBAN DE89"                          | Exact text matching                |
| Combined search   | "invoice over 5000 euros"            | Semantics + keywords               |

## Semantic search

The AI understands:

- **Synonyms**: "salary" also finds "compensation", "wages", "remuneration"
- **Context**: "termination period" also finds passages about contract ending
- **Multilingual**: English queries also find German documents and vice versa

## Filters

- **Workspace filter**: Restrict search to a specific workspace
- **Pagination**: Browse through large result sets with `limit` and `offset`

## Tips

- Natural questions often yield better results than single keywords
- `global_search` automatically combines full-text search with semantic search
- For precise results: use workspace filter
- Score values > 0.8 are considered very good matches
