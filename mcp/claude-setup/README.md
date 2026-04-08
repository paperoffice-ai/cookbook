# MCP-Setup für Claude Desktop und Claude Code

Anleitung zum Anbinden des **PaperOffice MCP-Servers** an **Claude Desktop** und **Claude Code**. Nach der Einrichtung kann Claude PaperOffice-Tools direkt aufrufen — analog zur Nutzung in anderen MCP-fähigen Umgebungen.

## Verifizierter Endpoint

| Transport | URL |
|-----------|-----|
| SSE (Server-Sent Events) | `https://mcp.paperoffice.ai/claude` |

**Authentifizierung:** Bearer-Token über HTTP-Header oder Query-Parameter.

## Claude Desktop: `claude_desktop_config.json`

Die Konfigurationsdatei liegt je nach Betriebssystem im Anwendungsdaten-Ordner von Claude Desktop (Pfad in der offiziellen Anthropic-Dokumentation nachschlagen).

Eintrag für PaperOffice:

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

Ersetze `your_api_key` durch deinen gültigen PaperOffice-API-Schlüssel. Nach Speichern Claude Desktop neu starten, damit MCP-Server geladen werden.

## Claude Code

**Claude Code** (CLI / IDE-Integration) verwendet ebenfalls eine MCP-Server-Liste — strukturell ähnlich wie bei Claude Desktop: Remote-Server mit `url` und `headers` für `Authorization`.

- Trage denselben Server ein wie oben (`https://mcp.paperoffice.ai/claude`, Bearer-Token).
- Konkreter Dateipfad und JSON-Schema können sich je nach Claude-Code-Version unterscheiden; bitte die **aktuelle Anthropic-Dokumentation zu Claude Code + MCP** verwenden und die Felder (`mcpServers`, `url`, `headers`) analog setzen.

## Verhalten

- Claude kann **PaperOffice-Tools direkt aufrufen** (z. B. OCR, IDP, Übersetzung), sobald die MCP-Verbindung steht.
- Die Toolauswahl erfolgt im Dialog — du beschreibst das Ziel, Claude wählt passende Tools aus der bereitgestellten Liste.

## Artefakte-Modus (Hinweis)

Im **Artefakte-Modus** von Claude lassen sich Ergebnisse aus Tool-Aufrufen (z. B. **OCR-Text** oder strukturierte Ausgaben) oft direkt weiterverarbeiten: Zusammenfassungen, Tabellen, Nachbearbeitung oder Einbindung in längere Antworten — ohne die Rohdaten manuell zwischen Fenstern zu kopieren.

## Troubleshooting

1. **Konfigurationspfad:** Falsche Datei oder JSON-Syntaxfehler — Desktop-Log bzw. Entwicklertools prüfen.
2. **Token:** Gültigkeit und Schreibweise `Bearer your_api_key` prüfen.
3. **Health:** `GET https://mcp.paperoffice.ai/health` zur schnellen Verfügbarkeitsprüfung.

## Weitere URLs (Referenz)

| Zweck | URL |
|-------|-----|
| Cursor | `https://mcp.paperoffice.ai/cursor` |
| OpenAI / ChatGPT | `https://mcp.paperoffice.ai/openai` |
| Standard-MCP | `https://mcp.paperoffice.ai/mcp` |
| Universal / Übersicht | `https://mcp.paperoffice.ai/` |

Für Claude ist der Eintrag **`/claude`** die passende URL.
