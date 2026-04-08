# Textübersetzung

Übersetzt Texte zwischen über 100 Sprachen. Drei Qualitätsstufen verfügbar: `basic` (schnell), `premium` (ausgewogen) und `ultra` (höchste Qualität). Automatische Quellsprach-Erkennung.

## Voraussetzungen

```bash
export PAPEROFFICE_API_KEY=po_sk_xxx
```

## Quick Start

```bash
# cURL
bash example.sh "Hello World" de
bash example.sh "Bonjour le monde" de fr premium

# Python (benötigt: pip install requests)
python example.py "Hello World" de
python example.py "Hello World" de auto ultra

# Node.js 18+
node example.js "Hello World" de
node example.js "Hello World" de auto ultra
```

## Endpoints

### Textübersetzung

```
POST https://api.paperoffice.ai/latest/translate/text
```

### Unterstützte Sprachen abfragen

```
GET https://api.paperoffice.ai/latest/translate/languages
```

## Parameter (Textübersetzung)

| Parameter | Typ | Pflicht | Default | Beschreibung |
|---|---|---|---|---|
| `text` | string | ✅ | — | Zu übersetzender Text |
| `target_language` | string | ✅ | — | Zielsprache (z.B. `de`, `en`, `fr`, `es`) |
| `source_language` | string | — | `auto` | Quellsprache (`auto` = automatische Erkennung) |
| `tier` | string | — | `premium` | Qualitätsstufe: `basic`, `premium` oder `ultra` |

## Qualitätsstufen

| Tier | Geschwindigkeit | Qualität | Empfehlung |
|---|---|---|---|
| `basic` | ⚡ Schnell | Gut | Bulk-Übersetzungen, Vorschau |
| `premium` | ⚡ Schnell | Sehr gut | Standard für die meisten Anwendungsfälle |
| `ultra` | 🐢 Langsamer | Exzellent | Veröffentlichungen, rechtliche Texte |

## Response-Beispiel

```json
{
  "status": "success",
  "data": {
    "translation": "Hallo Welt",
    "source_language": "en",
    "target_language": "de",
    "tier": "premium",
    "characters": 11
  }
}
```

## Tipps

- **Automatische Erkennung:** `source_language=auto` erkennt die Quellsprache zuverlässig
- **Kosten:** `basic` ist am günstigsten, `ultra` am teuersten — wähle passend zum Anwendungsfall
- **Sprachen-Liste:** `GET /translate/languages` gibt alle unterstützten Sprach-Codes zurück
