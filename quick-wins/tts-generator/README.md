# Text-to-Speech Generator

Generiert natürlich klingende Sprache aus Text mit neuronalen Stimmen. Über 100 Stimmen in vielen Sprachen.

## Voraussetzungen

```bash
export PAPEROFFICE_API_KEY=po_sk_xxx
```

## Quick Start

```bash
# cURL
bash example.sh "Hallo Welt" Nadja

# Python
pip install requests
python example.py "Hallo Welt" Nadja

# Node.js
npm install form-data
node example.js "Hallo Welt" Nadja
```

## Deutsche Stimmen

| Stimme | Beschreibung |
|---|---|
| `Nadja` | Weiblich, natürlich (empfohlen) |
| `Thomas` | Männlich, professionell |
| `Anna` | Weiblich, warm |
| `Hans` | Männlich, neutral |

## API-Details

| Parameter | Wert | Beschreibung |
|---|---|---|
| `Authorization` | `Bearer po_sk_xxx` | **Erforderlich** |
| `text` | Freitext | Zu sprechender Text |
| `voice` | `Nadja` | Stimme auswählen |
| `output_format` | `mp3` / `wav` | Audio-Format |
| `output` | `url` / `base64` / `inline` | Ausgabeformat |
| `speed` | `1.0` | Geschwindigkeit (0.5–2.0) |
| `priority` | `999` | Sync für TTS (immer 999) |
