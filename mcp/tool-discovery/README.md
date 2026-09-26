# Tool Discovery — Finding PaperOffice Tools via MCP

The PaperOffice MCP server exposes **300+ API/MCP tools**. Most lanes keep `tools/list`
short on purpose and reach the rest through discovery tools. This guide shows how that
works.

## Lanes and what `tools/list` returns

| URL | `tools/list` | Reach the rest via |
|-----|--------------|--------------------|
| `https://mcp.paperoffice.ai/claude` | full Documents Operations catalog (Directory without TTS) | direct `tools/call` |
| `https://mcp.paperoffice.ai/mcp-full` | every module (Documents, media, CRM, telephony) | direct `tools/call` |
| `https://mcp.paperoffice.ai/dms`, `/cursor`, `/grok` | core tools + 4 discovery tools | `po_mcp_tools_search` → `call_read` / `call_write` |
| `https://mcp.paperoffice.ai/chatgpt` (alias `/openai`) | 5 core tools + 4 discovery tools | `po_mcp_tools_search` → `call_read` / `call_write` |
| `https://mcp.paperoffice.ai/mcp` | slim read-safe IDE subset | switch to `/dms` or `/mcp-full` for more |

**Transport:** Streamable HTTP. **Auth:** OAuth 2.1 (Claude, ChatGPT, Grok) or a
bearer header with a user/group token (`po_ut_` / `po_gt_`). `po_sk_` and `po_pk_` are
rejected.

## The four discovery tools

| Tool | Effect |
|------|--------|
| `po_mcp_tools_search` | Read-only. Natural-language search over the catalog; returns `tool_id`, a one-liner, annotations and `execute_via`. |
| `po_mcp_tools_schema` | Read-only. Full input contract of one `tool_id`. |
| `po_mcp_tools_call_read` | Runs read-only inner tools. Writes are rejected with `TOOL_WRITE_REQUIRED`. |
| `po_mcp_tools_call_write` | Runs inner tools that create, change, delete or send. |

Inner `tool_id`s (for example `po_vat_validate`, `po_pdfstudio_merge`,
`po_storage_mounts_list`) are **not** native tools on discovery lanes. Calling them
directly returns `TOOL_UNKNOWN`; go through the dispatcher instead.

## Example: validate a VAT number on `/cursor`

```json
{ "method": "tools/call", "params": { "name": "po_mcp_tools_search", "arguments": { "query": "validate EU VAT number" } } }
```

The hit names `po_vat_validate` with `execute_via: po_mcp_tools_call_read`. Then:

```json
{ "method": "tools/call", "params": { "name": "po_mcp_tools_call_read", "arguments": { "tool_id": "po_vat_validate", "arguments": { "vat_id": "DE123456789" } } } }
```

## What each tool carries

| Field | Meaning |
|-------|---------|
| `name` / `tool_id` | invocation identifier |
| `description` | starts with `READ-ONLY.`, `WRITES DATA.` or `DESTRUCTIVE.` |
| `inputSchema` | JSON Schema of the arguments |
| `annotations` | `readOnlyHint`, `destructiveHint`, `openWorldHint` |
| `outputSchema` | shape of `structuredContent` (ChatGPT lane) |

## Relation to the REST API

The catalog mirrors the REST API. For machine-readable REST docs use
`https://api.paperoffice.ai/latest/docs/llms.txt`; the Postman collection at
`https://api.paperoffice.ai/latest/docs/postman` is generated live from the same source.

## Quick checklist

1. Pick the lane for your client (table above).
2. Sign in with OAuth or set the bearer token.
3. `tools/list` for the core; `po_mcp_tools_search` for everything else.
4. Read the effect marker before calling a write tool.
