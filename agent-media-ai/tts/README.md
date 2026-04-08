# Text-to-Speech (TTS)

Converts text to natural-sounding speech. Over 100 neural voices available in numerous languages. Synchronous processing with `priority ≥ 900`.

## Prerequisites

```bash
export PAPEROFFICE_API_KEY=po_sk_xxx
```

## Quick Start

```bash
# cURL
bash example.sh "Hallo Welt" Nadja mp3

# Python (requires: pip install requests)
python example.py "Hallo Welt" Nadja mp3

# Node.js 18+
node example.js "Hallo Welt" Nadja mp3
```

## Endpoint

```
POST https://api.paperoffice.ai/latest/job/add/paperoffice_voice___tts
```

## Parameters

| Parameter | Type | Required | Default | Description |
|---|---|---|---|---|
| `text` | string | ✅ | — | Text to be spoken |
| `voice` | string | — | `Nadja` | Select voice (see table) |
| `output_format` | string | — | `mp3` | `mp3` or `wav` |
| `output` | string | — | `url` | `url`, `base64` or `inline` |
| `speed` | float | — | `1.0` | Speed (0.5–2.0) |
| `priority` | int | — | — | `≥ 900` for synchronous processing |
| `language` | string | — | auto | Language code (e.g. `de`, `en`) — auto-detected |

## German Voices

| Voice | Gender | Description |
|---|---|---|
| `Nadja` | Female | Natural, warm (recommended) |
| `Thomas` | Male | Professional, clear |
| `Anna` | Female | Friendly, versatile |
| `Hans` | Male | Neutral, factual |

## Response Example

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

## Tips

- **Synchronous processing:** `priority=900` or higher returns the result directly in the response
- **Force language:** With `language=en` you can override the automatic language detection
- **Long texts:** For texts > 5000 characters, asynchronous processing (without priority) is recommended
