# MCP-Setup für ChatGPT (OpenAI) und Custom GPTs

Anleitung zur Nutzung des **PaperOffice MCP-Servers** mit **ChatGPT**, **Custom GPTs** und OpenAI-nahen Integrationen. Der dedizierte Endpoint ist für die OpenAI-Ökosysteme vorgesehen.

## Verifizierter Endpoint

| Zweck | URL |
|-------|-----|
| ChatGPT / OpenAI | `https://mcp.paperoffice.ai/openai` |

**Transport:** SSE (Server-Sent Events), wie bei allen PaperOffice-MCP-Endpunkten.

**Authentifizierung:** API-Key als **Bearer-Token** (HTTP-Header `Authorization: Bearer your_api_key` oder alternativ Query-Parameter, sofern vom jeweiligen Client unterstützt).

## Custom GPT als Action

1. **Action-URL:** Verwende `https://mcp.paperoffice.ai/openai` als Basis für die Verbindung zu PaperOffice (je nach GPT-Builder: „OpenAPI“-basierte Action oder vergleichbare MCP-Anbindung).
2. **Schema:** Das **OpenAPI-Schema** (bzw. die vom MCP-Server bereitgestellte Schnittstellenbeschreibung) wird **automatisch vom MCP-Server** bereitgestellt — keine manuelle Pflege einer statischen Postman-Datei im Cookbook nötig.
3. **Auth:** Trage den PaperOffice-API-Key als Bearer-Token ein; in manchen Oberflächen als „API Key“ mit Präfix oder als reines Secret — konsistent mit der Bearer-Vorgabe halten.

Hinweis: Die genaue Oberfläche von ChatGPT / GPT-Store ändert sich; falls „Actions“ nur klassische REST-OpenAPI ohne MCP erwarten, die **aktuelle OpenAI-Dokumentation** zu Actions und MCP prüfen und die bereitgestellte Schema-URL verwenden.

## Nutzung über API

Wenn du programmatisch gegen OpenAI und parallel PaperOffice-MCP arbeitest:

- Verbinde deinen Stack mit `https://mcp.paperoffice.ai/openai` und dem Bearer-Token.
- Nutze die vom Server exponierten MCP-Methoden (z. B. `tools/list`, `tools/call`) entsprechend dem MCP-Standard — siehe Rezept **Tool-Discovery** im selben Cookbook-Verzeichnis.

## Sicherheit

- API-Keys **nicht** in öffentlichen Repositories oder Screenshots abbilden.
- Keys regelmäßig rotieren und nur mit minimal nötigen Berechtigungen verwenden.

## Referenz: andere MCP-URLs

| Client-Typ | URL |
|------------|-----|
| Cursor | `https://mcp.paperoffice.ai/cursor` |
| Claude | `https://mcp.paperoffice.ai/claude` |
| Standard-MCP | `https://mcp.paperoffice.ai/mcp` |
| Universal | `https://mcp.paperoffice.ai/` |

Für ChatGPT und OpenAI-nahe Setups ist **`/openai`** die passende URL.
