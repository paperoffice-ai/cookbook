# Cursor — MCP Setup

**Tool:** Cursor IDE | **Output:** MCP Server Config + IDE-native Document AI

## Prompt

Kopiere diesen Prompt direkt in Cursor:

```
Read this API documentation:
https://api.paperoffice.ai/latest/docs/postman

Help me set up the MCP Server for PaperOffice in Cursor.
I want to use Document AI directly in my IDE.

Show me:
1. How to configure the MCP connection
2. Available tools via tools/list
3. How to process documents from my workspace
```

## MCP-Konfiguration

Füge dies in deine `.cursor/mcp.json` ein:

```json
{
  "mcpServers": {
    "paperoffice": {
      "url": "https://mcp.paperoffice.ai/cursor",
      "headers": {
        "Authorization": "Bearer YOUR_API_KEY"
      }
    }
  }
}
```

### MCP-URLs nach Client

| Client | URL |
|---|---|
| **Cursor IDE** | `https://mcp.paperoffice.ai/cursor` |
| **Claude Desktop / Claude Code** | `https://mcp.paperoffice.ai/claude` |
| **Standard MCP** | `https://mcp.paperoffice.ai/mcp` |
| **OpenAI / ChatGPT** | `https://mcp.paperoffice.ai/openai` |

## Was du bekommst

- Vollständige MCP-Konfiguration für Cursor
- Liste aller verfügbaren Document-AI-Tools (~409 Tools)
- Beispiele wie du Dokumente direkt aus dem Workspace verarbeitest
