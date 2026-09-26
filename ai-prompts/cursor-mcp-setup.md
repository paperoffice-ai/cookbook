# Cursor — MCP Setup

**Tool:** Cursor IDE | **Output:** MCP Server Config + IDE-native Document AI

## Prompt

Copy this prompt directly into Cursor:

```
Read this API guide first, completely:
https://api.paperoffice.ai/latest/docs/llms.txt
Use the Postman collection at https://api.paperoffice.ai/latest/docs/postman only for exact request and response samples.

Help me set up the MCP Server for PaperOffice in Cursor.
I want to use Document AI directly in my IDE.

Show me:
1. How to configure the MCP connection
2. Available tools via tools/list
3. How to process documents from my workspace
```

## MCP Configuration

Add this to your `.cursor/mcp.json`:

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

### MCP URLs by Client

| Client | URL |
|---|---|
| **Cursor / Windsurf** | `https://mcp.paperoffice.ai/cursor` |
| **Claude Desktop / Claude Code** | `https://mcp.paperoffice.ai/claude` |
| **ChatGPT** | `https://mcp.paperoffice.ai/chatgpt` |
| **Grok** | `https://mcp.paperoffice.ai/grok` |
| **Headless DMS** | `https://mcp.paperoffice.ai/dms` |

## What you get

- Complete MCP configuration for Cursor
- The core tools plus `po_mcp_tools_search` to reach the rest of the 300+ catalog
- Examples of how to process documents directly from the workspace
