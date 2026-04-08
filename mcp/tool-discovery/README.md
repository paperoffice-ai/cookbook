# Tool Discovery — Available PaperOffice Tools via MCP

This guide describes how to **find available tools** on the PaperOffice MCP server, what **metadata** each tool has, and how to access them via the **MCP standard**. The PaperOffice platform currently bundles **357+ API tools** (the exact list is provided live by the server and grows over time).

## Getting Started: Universal Root

**GET** the base URL to get an **overview**:

```
https://mcp.paperoffice.ai/
```

This route serves as the **discovery** entry point: which tools (or interfaces) are offered, typically **grouped by category** — common areas include **IDP**, **OCR**, **TTS**, **STT**, **Translation** and more, as described in the API documentation.

**Authentication:** Bearer token (`Authorization: Bearer your_api_key`) or query parameter, depending on client.

## What each tool typically contains

For each tool you should find (via MCP or the provided metadata) the following:

| Aspect | Meaning |
|--------|---------|
| **Name** | Unique tool name (invocation identifier). |
| **Description** | Short description of what the tool is for. |
| **Parameter Schema** | Input parameters in structured form (e.g. JSON Schema). |
| **Examples** | Example calls or example payloads, where provided. |

This lets you check in advance which tools fit your use case without manually sifting through the full REST documentation.

## MCP Standard: `tools/list` and `tools/call`

The **Model Context Protocol** defines, among other things:

- **`tools/list`** — List of all tools the connected MCP server offers (including names and descriptions, schema depending on server).
- **`tools/call`** — Execute a specific tool with the provided arguments.

Specific message formats and fields follow the MCP specification and the PaperOffice server implementation; in practice, you connect via **SSE** to one of the endpoints (e.g. `https://mcp.paperoffice.ai/mcp` for Standard MCP) and execute the JSON-RPC or protocol-specific calls your client supports.

## Relation to the REST API

The **357+ tools** mirror the **API tool landscape** of the PaperOffice platform (endpoints from the central source). MCP is an **additional access layer** for AI clients; the functional meaning of the tools (OCR, IDP, …) is the same as with direct API calls.

For deeper REST details (individual paths, rate limits), refer to the **current API documentation** at `https://api.paperoffice.ai/latest/docs/postman` — the collection is dynamically generated and is the canonical reference.

## Endpoints at a Glance

| Purpose | URL |
|---------|-----|
| Universal / Discovery Start | `https://mcp.paperoffice.ai/` |
| Cursor | `https://mcp.paperoffice.ai/cursor` |
| Claude | `https://mcp.paperoffice.ai/claude` |
| OpenAI / ChatGPT | `https://mcp.paperoffice.ai/openai` |
| Standard MCP | `https://mcp.paperoffice.ai/mcp` |

All listed endpoints support **SSE transport**; authentication is consistently via **Bearer token** (header or query).

## Quick Checklist

1. Obtain and securely store your token.
2. Use `GET https://mcp.paperoffice.ai/` for the overview (or `tools/list` via MCP).
3. Select the matching tool by schema and description.
4. Execute with `tools/call` or the respective client.
