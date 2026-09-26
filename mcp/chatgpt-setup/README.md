# MCP Setup for ChatGPT

Connect ChatGPT to PaperOffice through the dedicated ChatGPT lane of the hosted MCP server.

## Endpoint

| Purpose | URL |
|---------|-----|
| ChatGPT connector | `https://mcp.paperoffice.ai/chatgpt` |
| Legacy alias | `https://mcp.paperoffice.ai/openai` |

**Transport:** Streamable HTTP (remote MCP). No local process.

**Authentication:** OAuth 2.1. ChatGPT opens the PaperOffice sign-in page on the first
request; sign in with your PaperOffice account or paste a **user token** (`po_ut_…`) or
**group token** (`po_gt_…`) from [app.paperoffice.ai](https://app.paperoffice.ai). System
keys (`po_sk_`) and publishable keys (`po_pk_`) are rejected by the MCP server.

## What ChatGPT sees

The ChatGPT lane lists a small core plus four discovery tools:

- `po_workspaces_list`, `po_documents_search`, `po_documents_get`,
  `po_documents_create_from_content`, `po_job_get`
- `po_mcp_tools_search` → find any tool in the Documents Operations catalog
- `po_mcp_tools_schema` → read its contract
- `po_mcp_tools_call_read` → run read-only tools
- `po_mcp_tools_call_write` → run tools that create, change, delete or send

Every description starts with `READ-ONLY.`, `WRITES DATA.` or `DESTRUCTIVE.`.
Business documents only; do not store health records in connected workspaces.

## Add the connector

In ChatGPT go to **Settings → Connectors → Add** and paste
`https://mcp.paperoffice.ai/chatgpt`. Complete the OAuth sign-in. Then ask, for example:

```text
List my PaperOffice workspaces and the number of documents in each one.
Find the latest invoice and tell me the total amount and currency.
```

## Reference: other MCP URLs

| Client | URL |
|--------|-----|
| Claude Desktop / Anthropic Directory | `https://mcp.paperoffice.ai/claude` |
| Cursor / Windsurf | `https://mcp.paperoffice.ai/cursor` |
| Grok | `https://mcp.paperoffice.ai/grok` |
| Headless DMS (canonical) | `https://mcp.paperoffice.ai/dms` |
| Everything, all modules | `https://mcp.paperoffice.ai/mcp-full` |

Ready-made config files for every client:
[paperoffice-ai/paperoffice-mcp-setup](https://github.com/paperoffice-ai/paperoffice-mcp-setup).
