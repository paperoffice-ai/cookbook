# MCP-Setup für Cursor IDE

Anleitung zum Anbinden des **PaperOffice MCP-Servers** an die **Cursor IDE**. Nach erfolgreicher Konfiguration stehen alle PaperOffice-API-Tools direkt im KI-Chat zur Verfügung.

## Verifizierter Endpoint

| Transport | URL |
|-----------|-----|
| SSE (Server-Sent Events) | `https://mcp.paperoffice.ai/cursor` |

**Authentifizierung:** Bearer-Token über HTTP-Header oder Query-Parameter (`Authorization: Bearer <token>` bzw. entsprechender Query-Name je nach Client).

## Konfiguration: `.cursor/mcp.json`

Lege im Projektroot (oder in der Cursor-Konfiguration) eine Datei `.cursor/mcp.json` an bzw. ergänze sie um den Eintrag `paperoffice`:

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

Ersetze `your_api_key` durch deinen gültigen PaperOffice-API-Schlüssel.

## Was passiert danach?

- Cursor nutzt **SSE-Transport** für die Verbindung zum MCP-Server.
- Es stehen **alle 357 PaperOffice-Tools** (Stand Plattform) im KI-Kontext bereit — dieselbe Toolpalette wie über die REST-API, gebündelt über MCP.
- Du musst keine einzelnen Endpoints manuell im Chat referenzieren; das Modell kann passende Tools auswählen und aufrufen.

## Vorteile im Alltag

- **OCR, IDP, Übersetzung, TTS, STT** und weitere Kategorien direkt aus dem Editor heraus testen und automatisieren.
- Weniger Kontextwechsel: Experimente und kleine Pipelines bleiben in Cursor statt in separaten Skripten oder Postman.
- Konsistente Authentifizierung über denselben API-Key wie bei direkten API-Aufrufen.

## Troubleshooting

1. **API-Key:** Prüfe, ob der Key aktiv ist, zum richtigen Konto gehört und nicht abgelaufen ist. Header muss exakt `Bearer <token>` sein (Leerzeichen nach `Bearer`).
2. **Erreichbarkeit:** Prüfe den Server-Status mit `GET https://mcp.paperoffice.ai/health` (oder dem in eurer Umgebung dokumentierten Health-Pfad auf dem MCP-Host).
3. **Netzwerk / Proxy:** Firewalls oder TLS-Inspektion können SSE-Verbindungen stören — ggf. Ausnahmen für `mcp.paperoffice.ai` setzen.
4. **Cursor-Version:** Stelle sicher, dass die installierte Cursor-Version MCP mit Remote-URL und SSE unterstützt; bei Problemen Release Notes prüfen.

## Weitere Endpunkte (Überblick)

| Zweck | URL |
|-------|-----|
| Claude-optimiert | `https://mcp.paperoffice.ai/claude` |
| OpenAI / ChatGPT | `https://mcp.paperoffice.ai/openai` |
| Standard-MCP | `https://mcp.paperoffice.ai/mcp` |
| Universal | `https://mcp.paperoffice.ai/` |

Für Cursor ist der Eintrag **`/cursor`** die passende URL.
