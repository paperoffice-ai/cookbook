# Text-to-Speech (TTS)

Wandelt Text in natürlich klingende Sprache um. Über 100 neuronale Stimmen in zahlreichen Sprachen verfügbar. Synchrone Verarbeitung mit `priority ≥ 900`.

## Voraussetzungen

```bash
export PAPEROFFICE_API_KEY=po_sk_xxx
```

## Quick Start

```bash
# cURL
bash example.sh "Hallo Welt" Nadja mp3

# Python (benötigt: pip install requests)
python example.py "Hallo Welt" Nadja mp3

# Node.js 18+
node example.js "Hallo Welt" Nadja mp3
```

## Endpoint

```
POST https://api.paperoffice.ai/latest/job/add/paperoffice_voice___tts
```

## Parameter

| Parameter | Typ | Pflicht | Default | Beschreibung |
|---|---|---|---|---|
| `text` | string | ✅ | — | Zu sprechender Text |
| `voice` | string | — | `Nadja` | Stimme auswählen (siehe Tabelle) |
| `output_format` | string | — | `mp3` | `mp3` oder `wav` |
| `output` | string | — | `url` | `url`, `base64` oder `inline` |
| `speed` | float | — | `1.0` | Geschwindigkeit (0.5–2.0) |
| `priority` | int | — | — | `≥ 900` für synchrone Verarbeitung |
| `language` | string | — | auto | Sprach-Code (z.B. `de`, `en`) — wird automatisch erkannt |

## Deutsche Stimmen

| Stimme | Geschlecht | Beschreibung |
|---|---|---|
| `Nadja` | Weiblich | Natürlich, warm (empfohlen) |
| `Thomas` | Männlich | Professionell, klar |
| `Anna` | Weiblich | Freundlich, vielseitig |
| `Hans` | Männlich | Neutral, sachlich |

## Response-Beispiel

```json
{
  "status": "success",
  "result": {
    "status": "completed",
    "audio_url": "https://api-c2.paperoffice.ai:44376/latest/binary_download.php?file=...",
    "audio_duration_seconds": 1.332,
    "voice": "Nadja",
    "language": "de",
    "audio_size": 33270,
    "output_mode": "url"
  }
}
```

## Tipps

- **Synchron arbeiten:** `priority=900` oder höher liefert das Ergebnis direkt in der Response
- **Sprache erzwingen:** Mit `language=en` kann die automatische Spracherkennung überschrieben werden
- **Lange Texte:** Für Texte > 5000 Zeichen empfiehlt sich asynchrone Verarbeitung (ohne priority)
