# Text Translation

Translates text between over 100 languages. Three quality tiers available: `basic` (fast), `premium` (balanced) and `ultra` (highest quality). Automatic source language detection.

## Prerequisites

```bash
export PAPEROFFICE_API_KEY=po_sk_xxx
```

## Quick Start

```bash
# cURL
bash example.sh "Hello World" de
bash example.sh "Bonjour le monde" de fr premium

# Python (requires: pip install requests)
python example.py "Hello World" de
python example.py "Hello World" de auto ultra

# Node.js 18+
node example.js "Hello World" de
node example.js "Hello World" de auto ultra
```

## Endpoints

### Text Translation

```
POST https://api.paperoffice.ai/latest/translate/text
```

### List Supported Languages

```
GET https://api.paperoffice.ai/latest/translate/languages
```

## Parameters (Text Translation)

| Parameter | Type | Required | Default | Description |
|---|---|---|---|---|
| `text` | string | ✅ | — | Text to translate |
| `target_language` | string | ✅ | — | Target language (e.g. `de`, `en`, `fr`, `es`) |
| `source_language` | string | — | `auto` | Source language (`auto` = automatic detection) |
| `tier` | string | — | `premium` | Quality tier: `basic`, `premium` or `ultra` |

## Quality Tiers

| Tier | Speed | Quality | Recommendation |
|---|---|---|---|
| `basic` | ⚡ Fast | Good | Bulk translations, preview |
| `premium` | ⚡ Fast | Very good | Standard for most use cases |
| `ultra` | 🐢 Slower | Excellent | Publications, legal texts |

## Response Example

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

## Tips

- **Automatic detection:** `source_language=auto` reliably detects the source language
- **Cost:** `basic` is the cheapest, `ultra` the most expensive — choose according to use case
- **Language list:** `GET /translate/languages` returns all supported language codes
