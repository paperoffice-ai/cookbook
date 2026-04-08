# MCP Setup for ChatGPT (OpenAI) and Custom GPTs

Guide for using the **PaperOffice MCP Server** with **ChatGPT**, **Custom GPTs**, and OpenAI-related integrations. The dedicated endpoint is intended for the OpenAI ecosystem.

## Verified Endpoint

| Purpose | URL |
|---------|-----|
| ChatGPT / OpenAI | `https://mcp.paperoffice.ai/openai` |

**Transport:** SSE (Server-Sent Events), as with all PaperOffice MCP endpoints.

**Authentication:** API key as **Bearer token** (HTTP header `Authorization: Bearer your_api_key` or alternatively query parameter, if supported by the respective client).

## Custom GPT as Action

1. **Action URL:** Use `https://mcp.paperoffice.ai/openai` as the base for connecting to PaperOffice (depending on GPT Builder: "OpenAPI"-based Action or comparable MCP integration).
2. **Schema:** The **OpenAPI schema** (or the interface description provided by the MCP server) is **automatically provided by the MCP server** — no manual maintenance of a static Postman file in the Cookbook needed.
3. **Auth:** Enter the PaperOffice API key as Bearer token; in some interfaces as "API Key" with prefix or as a plain secret — keep consistent with the Bearer specification.

Note: The exact ChatGPT / GPT Store interface changes over time; if "Actions" only expect classic REST-OpenAPI without MCP, check the **current OpenAI documentation** for Actions and MCP and use the provided schema URL.

## Usage via API

If you work programmatically with OpenAI and PaperOffice MCP in parallel:

- Connect your stack to `https://mcp.paperoffice.ai/openai` with the Bearer token.
- Use the MCP methods exposed by the server (e.g. `tools/list`, `tools/call`) according to the MCP standard — see the **Tool Discovery** recipe in the same Cookbook directory.

## Security

- **Do not** expose API keys in public repositories or screenshots.
- Rotate keys regularly and use only with minimally required permissions.

## Reference: Other MCP URLs

| Client Type | URL |
|-------------|-----|
| Cursor | `https://mcp.paperoffice.ai/cursor` |
| Claude | `https://mcp.paperoffice.ai/claude` |
| Standard MCP | `https://mcp.paperoffice.ai/mcp` |
| Universal | `https://mcp.paperoffice.ai/` |

For ChatGPT and OpenAI-related setups, **`/openai`** is the appropriate URL.
