# MCP Setup for Claude Desktop and Claude Code

Guide for connecting the **PaperOffice MCP Server** to **Claude Desktop** and **Claude Code**. After setup, Claude can invoke PaperOffice tools directly — analogous to usage in other MCP-capable environments.

## Verified Endpoint

| Transport | URL |
|-----------|-----|
| SSE (Server-Sent Events) | `https://mcp.paperoffice.ai/claude` |

**Authentication:** Bearer token via HTTP header or query parameter.

## Claude Desktop: `claude_desktop_config.json`

The configuration file is located in the application data folder of Claude Desktop, depending on the operating system (refer to the official Anthropic documentation for the exact path).

Entry for PaperOffice:

```json
{
  "mcpServers": {
    "paperoffice": {
      "url": "https://mcp.paperoffice.ai/claude",
      "headers": {
        "Authorization": "Bearer your_api_key"
      }
    }
  }
}
```

Replace `your_api_key` with your valid PaperOffice API key. After saving, restart Claude Desktop so that MCP servers are loaded.

## Claude Code

**Claude Code** (CLI / IDE integration) also uses an MCP server list — structurally similar to Claude Desktop: remote server with `url` and `headers` for `Authorization`.

- Add the same server as above (`https://mcp.paperoffice.ai/claude`, Bearer token).
- The exact file path and JSON schema may differ depending on the Claude Code version; please refer to the **current Anthropic documentation for Claude Code + MCP** and set the fields (`mcpServers`, `url`, `headers`) accordingly.

## Behavior

- Claude can **invoke PaperOffice tools directly** (e.g. OCR, IDP, Translation) once the MCP connection is established.
- Tool selection happens in the dialog — you describe the goal, Claude selects matching tools from the provided list.

## Artifacts Mode (Note)

In Claude's **Artifacts mode**, results from tool calls (e.g. **OCR text** or structured outputs) can often be further processed directly: summaries, tables, post-processing, or embedding in longer responses — without manually copying raw data between windows.

## Troubleshooting

1. **Configuration path:** Wrong file or JSON syntax error — check the desktop log or developer tools.
2. **Token:** Verify validity and spelling `Bearer your_api_key`.
3. **Health:** `GET https://mcp.paperoffice.ai/health` for a quick availability check.

## Other URLs (Reference)

| Purpose | URL |
|---------|-----|
| Cursor | `https://mcp.paperoffice.ai/cursor` |
| OpenAI / ChatGPT | `https://mcp.paperoffice.ai/openai` |
| Standard MCP | `https://mcp.paperoffice.ai/mcp` |
| Universal / Overview | `https://mcp.paperoffice.ai/` |

For Claude, the **`/claude`** entry is the appropriate URL.
