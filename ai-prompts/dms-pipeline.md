# DMS Upload + Search Pipeline

**Tool:** Any AI Tool | **Output:** Complete DMS workflow — workspace, upload, smart search

## Prompt

```
Read this API documentation:
https://api.paperoffice.ai/latest/docs/postman

Build a Python DMS pipeline that:
1. Creates a workspace via POST /documents/workspaces-create (name, type, workspace_tier=standard)
2. Uploads PDF documents via POST /documents/document-put (file parameter, workspace_id)
3. Searches using POST /documents/documents-list with:
   - global_search = search term (string)
   - search_mode = intelligent (auto-selects best strategy, recommended)
   - Also supports search_mode=semantic, search_mode=hybrid, search_mode=fulltext
   - search_scope=all to search across all workspaces
4. For semantic/RAG search use POST /documents/document-search with query parameter
5. Returns results with relevance scores

Include:
- Bearer token authentication ($PAPEROFFICE_API_KEY)
- Error handling for all responses
- CLI interface: python dms_pipeline.py create|upload|search [args]
```

## What you get

A complete DMS pipeline that:
- Creates and configures workspaces (standard/confidential/compliance tiers)
- Uploads documents with automatic OCR processing
- Searches with 5 different modes for different use cases
- CLI-driven for easy integration into shell scripts

## Tips

- `workspace_tier=compliance` enables WORM (Write Once, Read Many) for regulated industries
- `search_mode=intelligent` on `/documents/documents-list` auto-selects the best strategy
- For RAG context retrieval, use `/documents/document-search` with `query` parameter
- Use `search_scope=all` to search across all workspaces
