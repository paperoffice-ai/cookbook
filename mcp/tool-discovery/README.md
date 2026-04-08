# Tool-Discovery — verfügbare PaperOffice-Tools über MCP

Diese Anleitung beschreibt, wie du **verfügbare Tools** auf dem PaperOffice-MCP-Server findest, welche **Metadaten** jedes Tool hat und wie du sie über den **MCP-Standard** ansteuerst. Die PaperOffice-Plattform bündelt derzeit **357 API-Tools** (Stand: Dokumentation zur API-/MCP-Landschaft); die genaue Liste wird live vom System bereitgestellt.

## Einstieg: Universal-Root

**GET** die Basis-URL, um eine **Übersicht** zu erhalten:

```
https://mcp.paperoffice.ai/
```

Diese Route dient der **Discovery**: Welche Tools (bzw. welche Schnittstellen) angeboten werden, in der Regel **nach Kategorien gruppiert** — typische Bereiche sind unter anderem **IDP**, **OCR**, **TTS**, **STT**, **Übersetzung** und weitere, wie in der API-Dokumentation beschrieben.

**Authentifizierung:** Bearer-Token (`Authorization: Bearer your_api_key`) oder Query-Parameter, je nach Client.

## Was jedes Tool typischerweise enthält

Für jedes Tool solltest du (über MCP bzw. die bereitgestellten Metadaten) folgendes finden:

| Aspekt | Bedeutung |
|--------|-----------|
| **Name** | Eindeutiger Tool-Name (Aufruf-Identifier). |
| **Beschreibung** | Kurzbeschreibung, wofür das Tool gedacht ist. |
| **Parameter-Schema** | Eingabeparameter in strukturierter Form (z. B. JSON-Schema). |
| **Beispiele** | Beispielaufrufe oder Beispielpayloads, wo bereitgestellt. |

So kannst du im Vorfeld prüfen, welche Tools für deinen Use Case passen, ohne alle 357 Einträge manuell durch die REST-Dokumentation zu jagen.

## MCP-Standard: `tools/list` und `tools/call`

Der **Model Context Protocol** definiert u. a.:

- **`tools/list`** — Liste aller Tools, die der verbundene MCP-Server anbietet (inkl. Namen und Beschreibungen, Schema je nach Server).
- **`tools/call`** — Ausführung eines konkreten Tools mit den übergebenen Argumenten.

Konkrete Nachrichtenformate und Felder richten sich nach der MCP-Spezifikation und der PaperOffice-Serverimplementierung; in der Praxis verbindet du dich per **SSE** zu einem der Endpunkte (z. B. `https://mcp.paperoffice.ai/mcp` für Standard-MCP) und führst die JSON-RPC- oder protokollspezifischen Aufrufe aus, die dein Client unterstützt.

## Bezug zur REST-API

Die **357 Tools** spiegeln die **API-Tool-Landschaft** der PaperOffice-Plattform wider (Endpoints aus der zentralen Quelle). MCP ist eine **zusätzliche Zugriffsschicht** für KI-Clients; die fachliche Bedeutung der Tools (OCR, IDP, …) ist dieselbe wie bei direkten API-Aufrufen.

Für tiefergehende REST-Details (einzelne Pfade, Rate Limits) die **aktuelle API-Dokumentation** unter `https://api.paperoffice.ai/latest/docs/postman` heranziehen — die Collection wird dynamisch erzeugt und ist die kanonische Referenz.

## Endpunkte auf einen Blick

| Zweck | URL |
|-------|-----|
| Universal / Discovery-Start | `https://mcp.paperoffice.ai/` |
| Cursor | `https://mcp.paperoffice.ai/cursor` |
| Claude | `https://mcp.paperoffice.ai/claude` |
| OpenAI / ChatGPT | `https://mcp.paperoffice.ai/openai` |
| Standard-MCP | `https://mcp.paperoffice.ai/mcp` |

Alle genannten Endpunkte unterstützen **SSE-Transport**; Authentifizierung erfolgt durchgehend per **Bearer-Token** (Header oder Query).

## Kurz-Checkliste

1. Token beschaffen und sicher aufbewahren.
2. `GET https://mcp.paperoffice.ai/` für die Übersicht nutzen (oder `tools/list` über MCP).
3. Passendes Tool per Schema und Beschreibung auswählen.
4. Mit `tools/call` oder dem jeweiligen Client ausführen.
