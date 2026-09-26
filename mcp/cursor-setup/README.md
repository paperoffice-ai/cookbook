# MCP Setup for Cursor IDE

Connect the PaperOffice MCP server to Cursor. Afterwards the agent can search, read and
create documents in your PaperOffice account, and reach the whole Documents Operations
catalog through discovery tools.

## Endpoint

| Transport | URL |
|-----------|-----|
| Streamable HTTP | `https://mcp.paperoffice.ai/cursor` |

**Authentication:** bearer header with a **user token** (`po_ut_…`) or **group token**
(`po_gt_…`) from [app.paperoffice.ai](https://app.paperoffice.ai) → *Account → API*.
A group token limits the connection to the workspaces of that group. System keys
(`po_sk_`) and publishable keys (`po_pk_`) are rejected by the MCP server.

## Option A — Cursor Marketplace plugin

Install **PaperOffice** from the Cursor Marketplace and set the plugin variable
`PAPEROFFICE_TOKEN` when asked. Nothing else to configure. Source:
[paperoffice-ai/paperoffice-cursor-plugin](https://github.com/paperoffice-ai/paperoffice-cursor-plugin).

## Option B — `.cursor/mcp.json`

```json
{
  "mcpServers": {
    "paperoffice": {
      "url": "https://mcp.paperoffice.ai/cursor",
      "headers": {
        "Authorization": "Bearer po_ut_..."
      }
    }
  }
}
```

Replace `po_ut_...` with your token and reload the window.

## What Cursor sees

`tools/list` on `/cursor` is short on purpose: `po_workspaces_list`, `po_documents_search`,
`po_documents_get`, `po_documents_text_get`, `po_documents_folders_list`,
`po_documents_tags_list`, `po_documents_create_from_content`,
`po_documents_upload_url_get`, `po_extraction_invoice`, `po_job_get`, plus the four
discovery tools `po_mcp_tools_search`, `po_mcp_tools_schema`, `po_mcp_tools_call_read`
and `po_mcp_tools_call_write`. Import, classification, signatures, storage, webhooks and
audit are reached through the discovery tools — see [Tool Discovery](../tool-discovery/).

Every description starts with `READ-ONLY.`, `WRITES DATA.` or `DESTRUCTIVE.`. The same
catalog is served on `/dms` and `/grok`. For media, CRM and telephony switch the URL to
`https://mcp.paperoffice.ai/mcp-full`.

## Troubleshooting

1. **401 on connect:** the header must be exactly `Bearer <token>`; the token must be
   active and of type `po_ut_` or `po_gt_`.
2. **Reachability:** `GET https://mcp.paperoffice.ai/health`.
3. **Proxy / TLS inspection:** allow `mcp.paperoffice.ai` and `api.paperoffice.ai`.
4. **Old Cursor build:** remote MCP over Streamable HTTP needs a current Cursor version.

## Other endpoints

| Purpose | URL |
|---------|-----|
| Claude Desktop / Anthropic Directory | `https://mcp.paperoffice.ai/claude` |
| ChatGPT | `https://mcp.paperoffice.ai/chatgpt` |
| Grok | `https://mcp.paperoffice.ai/grok` |
| Headless DMS (canonical) | `https://mcp.paperoffice.ai/dms` |
| Everything, all modules | `https://mcp.paperoffice.ai/mcp-full` |

Ready-made configs for every client:
[paperoffice-ai/paperoffice-mcp-setup](https://github.com/paperoffice-ai/paperoffice-mcp-setup).
