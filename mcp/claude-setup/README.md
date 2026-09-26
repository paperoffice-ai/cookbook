# MCP Setup for Claude Desktop, Claude Code and Claude Cowork

Connect the PaperOffice MCP server to Claude. Afterwards Claude can invoke PaperOffice
tools directly: search, read, OCR, extraction, classification, signatures, audit.

## Endpoint

| Transport | URL |
|-----------|-----|
| Streamable HTTP | `https://mcp.paperoffice.ai/claude` |

**Authentication:** OAuth 2.1. Claude opens the PaperOffice sign-in page on the first
request; sign in with your PaperOffice account or paste a **user token** (`po_ut_…`) or
**group token** (`po_gt_…`) from [app.paperoffice.ai](https://app.paperoffice.ai).
No token in the config file. System keys (`po_sk_`) and publishable keys (`po_pk_`) are
rejected.

## Claude Desktop

Add the server under **Settings → Connectors**, or in `claude_desktop_config.json`:

```json
{
  "mcpServers": {
    "paperoffice": {
      "url": "https://mcp.paperoffice.ai/claude"
    }
  }
}
```

Restart Claude Desktop and complete the OAuth sign-in when prompted.

## Claude Code / Claude Cowork

```bash
claude mcp add --transport http paperoffice https://mcp.paperoffice.ai/claude
```

For a headless setup with a token in the header use the canonical DMS lane instead:

```json
{
  "mcpServers": {
    "paperoffice": {
      "url": "https://mcp.paperoffice.ai/dms",
      "headers": { "Authorization": "Bearer po_ut_..." }
    }
  }
}
```

## What Claude sees

`/claude` lists the full **Documents Operations** catalog directly (Directory profile,
without text-to-speech). Every description starts with `READ-ONLY.`, `WRITES DATA.` or
`DESTRUCTIVE.`, and each tool carries `readOnlyHint`, `destructiveHint` and
`openWorldHint`. Claude asks for confirmation before destructive calls.

## Troubleshooting

1. **Sign-in loop:** allow `mcp.paperoffice.ai` and `api.paperoffice.ai` in the Claude.ai
   network allowlist (two **f**s).
2. **Health:** `GET https://mcp.paperoffice.ai/health`.
3. **Wrong token type:** `po_sk_` and `po_pk_` are rejected; create a `po_ut_` or `po_gt_`
   token.

## Other endpoints

| Purpose | URL |
|---------|-----|
| Cursor / Windsurf | `https://mcp.paperoffice.ai/cursor` |
| ChatGPT | `https://mcp.paperoffice.ai/chatgpt` |
| Grok | `https://mcp.paperoffice.ai/grok` |
| Headless DMS (canonical) | `https://mcp.paperoffice.ai/dms` |
| Everything, all modules | `https://mcp.paperoffice.ai/mcp-full` |

Ready-made configs for every client:
[paperoffice-ai/paperoffice-mcp-setup](https://github.com/paperoffice-ai/paperoffice-mcp-setup).
