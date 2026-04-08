# Smart Document Search — Complete Reference

PaperOffice DMS provides **5 search endpoints** with different capabilities: Ultimate Search (all-in-one), Semantic Search, Hybrid Search, Fulltext Search, and RAG Search.

## Endpoints overview

| Endpoint | Method | Best for |
|---|---|---|
| `/documents/list` | POST | **Ultimate Search** — intelligent auto-routing across all 4 search modes |
| `/documents/semantic-search` | POST | Pure vector-based semantic search |
| `/documents/search-hybrid` | POST | Combined fulltext + semantic |
| `/documents/search-fulltext` | POST | Traditional keyword search |
| `/documents/rag-search` | POST | RAG context retrieval (for AI/LLM pipelines) |

**Authentication:** Bearer Token (API key required)

---

## 1. Ultimate Search (recommended)

The most powerful endpoint — auto-detects the optimal search strategy.

```
POST https://api.paperoffice.ai/latest/documents/documents-list
```

### Parameters

| Parameter | Type | Required | Default | Description |
|---|---|---|---|---|
| `workspace_id` | int | **Yes** | — | ID of the workspace to search |
| `global_search` | string | No | — | Search term (triggers Ultimate Search across all 4 sources) |
| `search_mode` | string | No | `intelligent` | `intelligent` (auto-detect, recommended), `hybrid`, `semantic`, `fulltext` |
| `search_preference` | string | No | `balanced` | `keyword` (exact match priority), `semantic` (AI meaning priority), `balanced` (mix) |
| `search_scope` | string | No | `current` | `current` (this workspace only), `all` (all workspaces) |
| `similarity_threshold` | float | No | `0.35` | Minimum cosine similarity for semantic results (0.0–1.0) |
| `page` | int | No | `1` | Page number for pagination |
| `limit` | int | No | `500` | Documents per page (max 500) |
| `sort` | string | No | `created_datetime` | Sort field |
| `order` | string | No | `DESC` | `ASC` or `DESC` |

### Filters

| Filter | Type | Description |
|---|---|---|
| `__document__data__classification__document_type` | array | Filter by document types (JSON array or comma-separated) |
| `__document__content__extraction__keywords` | array | Filter by keywords |
| `__document__data__workflow__state` | array | Filter by workflow status |
| `__document__data__classification__locale` | array | Filter by language/locale |
| `__document__data__metadata__save_paths` | array | Filter by storage paths (`PREFIX_WILDCARD:/path` or `EXACT:/path`) |
| `ai_dms_status` | array | Filter by AI-DMS tier |
| `ai_agent_status` | array | Filter by AI-Agent status |
| `date_from` | string | From date (`YYYY-MM-DD`) |
| `date_to` | string | To date (`YYYY-MM-DD`) |
| `share_context` | string | Sharing context filter |

### Search modes explained

| Mode | How it works | Best for |
|---|---|---|
| `intelligent` | Automatically detects query type and routes to the best strategy | **General use (recommended)** |
| `hybrid` | Combines fulltext + semantic scoring | Best overall relevance |
| `semantic` | Pure vector search (meaning-based) | "Find docs about..." queries |
| `fulltext` | Traditional keyword matching | Exact IDs, reference numbers, IBANs |

### Example

```bash
curl -X POST "https://api.paperoffice.ai/latest/documents/list" \
  -H "Authorization: Bearer $PAPEROFFICE_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "workspace_id": 123,
    "global_search": "invoice from Acme over 5000 EUR",
    "search_mode": "intelligent",
    "search_preference": "balanced",
    "similarity_threshold": 0.35,
    "limit": 20
  }'
```

---

## 2. Semantic Search

Pure AI-powered vector search using embeddings.

```
POST https://api.paperoffice.ai/latest/documents/semantic-search
```

| Parameter | Type | Required | Default | Description |
|---|---|---|---|---|
| `query` | string | **Yes** | — | Natural language search query |
| `language` | string | No | all | Language filter (e.g., `de`, `en`). Null = all languages |
| `limit` | int | No | `10` | Maximum results (max 50) |
| `min_similarity` | float | No | `0.4` | Minimum cosine similarity (0.0–1.0) |
| `mode` | string | No | `auto` | `vector` (only vectors), `fulltext` (only text), `auto` (vector with fulltext fallback) |

**Understands:**
- **Synonyms**: "salary" finds "compensation", "wages", "remuneration"
- **Context**: "termination period" finds passages about contract ending
- **Multilingual**: English queries find German documents and vice versa

---

## 3. Hybrid Search

Combined fulltext + semantic scoring for best relevance.

```
POST https://api.paperoffice.ai/latest/documents/search-hybrid
```

| Parameter | Type | Required | Default | Description |
|---|---|---|---|---|
| `query` | string | **Yes** | — | Search term |
| `workspace_id` | int | No | — | Restrict to workspace |
| `limit` | int | No | `20` | Max results (1–100) |
| `offset` | int | No | `0` | Pagination offset |

---

## 4. Fulltext Search

Traditional keyword search (fastest, exact matches only).

```
POST https://api.paperoffice.ai/latest/documents/search-fulltext
```

| Parameter | Type | Required | Default | Description |
|---|---|---|---|---|
| `query` | string | **Yes** | — | Search term |
| `workspace_id` | int | No | — | Restrict to workspace |
| `limit` | int | No | `20` | Max results (1–100) |
| `offset` | int | No | `0` | Pagination offset |

---

## 5. RAG Search

Optimized for retrieving context chunks for AI/LLM pipelines.

```
POST https://api.paperoffice.ai/latest/documents/rag-search
```

| Parameter | Type | Required | Default | Description |
|---|---|---|---|---|
| `query` | string | No | — | Natural language search query |
| `limit` | int | No | `5` | Max results |
| `connector_types` | string | No | — | Filter by connector (comma-separated, e.g., `zammad`) |
| `source_types` | string | No | — | Filter by source type (e.g., `ticket,kb_article`) |

---

## How to run

```bash
export PAPEROFFICE_API_KEY="your_api_key"

# Bash — requires workspace_id (integer)
bash example.sh "contract terms" 42
bash example.sh "invoice 2026" 42 20

# Python
pip install requests
python3 example.py "contract terms" 42
python3 example.py "invoice 2026" 42 20

# Node.js
node example.js "contract terms" 42
node example.js "invoice 2026" 42 20
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

## Search strategy guide

| Goal | Endpoint | search_mode | search_preference |
|---|---|---|---|
| General search (don't know query type) | `/documents/documents-list` | `intelligent` | `balanced` |
| Find documents by meaning | `/documents/documents-list` | `semantic` | `semantic` |
| Find exact invoice number | `/documents/documents-list` | `fulltext` | `keyword` |
| Best overall relevance | `/documents/documents-list` | `hybrid` | `balanced` |
| AI/LLM context retrieval | `/documents/rag-search` | — | — |
| Score > 0.8 = very good match | any | — | — |

## Tips

- Natural questions often yield better results than single keywords
- Use `similarity_threshold` to control strictness (lower = more results, higher = more precise)
- For known document IDs or reference numbers, prefer `fulltext` mode
- `intelligent` mode is the best default — it auto-routes your query

## See also

- [DMS Upload](../document-upload/) — Upload documents to the DMS
- [Document Chat](../document-chat/) — Chat with documents
- [OCR Text-Mode](../../ocr/text-mode/) — Extract text for indexing
