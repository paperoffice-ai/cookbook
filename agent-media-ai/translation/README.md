# Text Translation

Translates text between 37 languages. Three quality tiers: `basic` (fast), `premium` (balanced), `ultra` (highest quality). Automatic source language detection.

## Endpoints

### Text Translation

```
POST https://api.paperoffice.ai/latest/translate/text
```

### List Supported Languages

```
GET https://api.paperoffice.ai/latest/translate/languages
```

**Authentication:** Bearer Token required

## How to run

```bash
export PAPEROFFICE_API_KEY="your_api_key"

# Bash
chmod +x example.sh && ./example.sh "Hello World" de
./example.sh "Bonjour le monde" de fr premium

# Python
pip install requests
python3 example.py "Hello World" de
python3 example.py "Hello World" de auto ultra

# Node.js (v18+)
node example.js "Hello World" de
node example.js "Hello World" de auto ultra
```

## Parameters (Text Translation)

| Parameter | Type | Required | Default | Description |
|---|---|---|---|---|
| `text` | string | **Yes** | — | Text to translate |
| `target_language` | string | **Yes** | — | Target language code (see table below) |
| `source_language` | string | No | `auto` | Source language (`auto` = automatic detection) |
| `tier` | string | No | `premium` | Quality tier: `basic`, `premium`, `ultra` |

## Quality tiers

| Tier | Speed | Quality | Cost | Best for |
|---|---|---|---|---|
| `basic` | Fastest | Good | Lowest | Bulk translations, internal previews |
| `premium` | Fast | Very good | Medium | Standard production use |
| `ultra` | Slower | Excellent | Highest | Publications, legal texts, marketing copy |

## Supported languages (37)

| Code | Language | Native name |
|---|---|---|
| `ar` | Arabic | العربية |
| `bg` | Bulgarian | Български |
| `cs` | Czech | Čeština |
| `da` | Danish | Dansk |
| `de` | German | Deutsch |
| `el` | Greek | Ελληνικά |
| `en` | English | English |
| `es` | Spanish | Español |
| `et` | Estonian | Eesti |
| `fi` | Finnish | Suomi |
| `fr` | French | Français |
| `he` | Hebrew | עברית |
| `hi` | Hindi | हिन्दी |
| `hr` | Croatian | Hrvatski |
| `hu` | Hungarian | Magyar |
| `id` | Indonesian | Bahasa Indonesia |
| `it` | Italian | Italiano |
| `ja` | Japanese | 日本語 |
| `ko` | Korean | 한국어 |
| `lt` | Lithuanian | Lietuvių |
| `lv` | Latvian | Latviešu |
| `ms` | Malay | Bahasa Melayu |
| `nl` | Dutch | Nederlands |
| `no` | Norwegian | Norsk |
| `pl` | Polish | Polski |
| `pt` | Portuguese | Português |
| `ro` | Romanian | Română |
| `ru` | Russian | Русский |
| `sk` | Slovak | Slovenčina |
| `sl` | Slovenian | Slovenščina |
| `sr` | Serbian | Српски |
| `sv` | Swedish | Svenska |
| `th` | Thai | ไทย |
| `tr` | Turkish | Türkçe |
| `uk` | Ukrainian | Українська |
| `vi` | Vietnamese | Tiếng Việt |
| `zh` | Chinese | 中文 |

## Response example

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
- **Cost optimization:** `basic` is the cheapest; use it for internal/preview translations
- **Best quality:** `ultra` is recommended for customer-facing, legal, or marketing content
- **Character count:** The `characters` field in the response shows billed characters
- **Language list:** `GET /translate/languages` returns the live list with flags and native names

## See also

- [Text-to-Speech](../tts/) — Convert translated text to speech
- [Speech-to-Text](../stt/) — Transcribe audio, then translate
