# MCP Setup for Cursor IDE

Guide for connecting the **PaperOffice MCP Server** to the **Cursor IDE**. After successful configuration, all PaperOffice API tools are available directly in the AI chat.

## Verified Endpoint

| Transport | URL |
|-----------|-----|
| SSE (Server-Sent Events) | `https://mcp.paperoffice.ai/cursor` |

**Authentication:** Bearer token via HTTP header or query parameter (`Authorization: Bearer <token>` or corresponding query name depending on client).

## Configuration: `.cursor/mcp.json`

Create or update a file `.cursor/mcp.json` in your project root (or in the Cursor configuration) with the `paperoffice` entry:

```json
{
  "mcpServers": {
    "paperoffice": {
      "url": "https://mcp.paperoffice.ai/cursor",
      "headers": {
        "Authorization": "Bearer your_api_key"
      }
    }
  }
}
```

Replace `your_api_key` with your valid PaperOffice API key.

## What happens next?

- Cursor uses **SSE transport** for the connection to the MCP server.
- **All 357+ PaperOffice tools** (as of current platform) are available in the AI context — the same tool palette as via the REST API, bundled through MCP.
- You don't need to manually reference individual endpoints in the chat; the model can select and invoke matching tools.

## Benefits in daily use

- **OCR, IDP, Translation, TTS, STT** and other categories can be tested and automated directly from the editor.
- Less context switching: experiments and small pipelines stay in Cursor instead of separate scripts or Postman.
- Consistent authentication using the same API key as for direct API calls.

## Troubleshooting

1. **API Key:** Check that the key is active, belongs to the correct account, and has not expired. The header must be exactly `Bearer <token>` (space after `Bearer`).
2. **Reachability:** Check the server status with `GET https://mcp.paperoffice.ai/health` (or the health path documented for your environment on the MCP host).
3. **Network / Proxy:** Firewalls or TLS inspection can disrupt SSE connections — set exceptions for `mcp.paperoffice.ai` if needed.
4. **Cursor Version:** Make sure the installed Cursor version supports MCP with remote URL and SSE; check the release notes if issues arise.

## Other Endpoints (Overview)

| Purpose | URL |
|---------|-----|
| Claude-optimized | `https://mcp.paperoffice.ai/claude` |
| OpenAI / ChatGPT | `https://mcp.paperoffice.ai/openai` |
| Standard MCP | `https://mcp.paperoffice.ai/mcp` |
| Universal | `https://mcp.paperoffice.ai/` |

For Cursor, the **`/cursor`** entry is the appropriate URL.
