# Text-to-Speech (TTS)

Converts text to natural-sounding speech using neural voices. Supports **39 languages**, multiple quality tiers, voice cloning, and multi-speaker output.

## Endpoint

```
POST https://api.paperoffice.ai/latest/job/add/paperoffice_voice___tts
```

**Authentication:** Bearer Token required

## How to run

```bash
export PAPEROFFICE_API_KEY="your_api_key"

# Bash — text, voice, language, format
chmod +x example.sh && ./example.sh "Hello world" Joanna en mp3

# Python
pip install requests
python3 example.py "Hello world" Joanna en mp3

# Node.js (v18+)
node example.js "Hello world" Joanna en mp3
```

## Parameters

| Parameter | Type | Required | Default | Description |
|---|---|---|---|---|
| `text` | string | **Yes** | — | Text to convert (max 50,000 characters) |
| `voice` | string | **Yes** | — | Voice name (see voice table below) |
| `language` | string | **Yes** | — | Language code (see language table below) |
| `quality` | string | No | `premium` | `basic` (fast), `premium` (balanced), `ultra` (best) |
| `output_format` | string | No | `mp3` | `mp3`, `wav`, `ogg` |
| `output` | string | No | `url` | `url`, `base64`, `inline` |
| `speed` | float | No | `1.0` | Speech speed: `0.9` (slower) to `1.1` (faster) |
| `temperature` | float | No | `0.9` | Sampling temperature: `0.1` (deterministic) to `1.0` (creative) |
| `top_p` | float | No | `0.7` | Nucleus sampling: `0.1` to `1.0` |
| `repetition_penalty` | float | No | `1.1` | Repetition penalty: `0.9` to `1.99` (higher = less repetition) |
| `priority` | int | No | `999` | `≥ 900` = synchronous (result inline) |

## Quality tiers

| Tier | Speed | Quality | Best for |
|---|---|---|---|
| `basic` | Fastest | Good | Previews, prototyping, bulk generation |
| `premium` | Fast | Very good | Standard production use |
| `ultra` | Slower | Excellent | Audiobooks, professional voice-overs |

## Supported languages (39)

| Code | Language | Code | Language | Code | Language |
|---|---|---|---|---|---|
| `ar` | Arabic | `hi` | Hindi | `pt-BR` | Portuguese (Brazil) |
| `bg` | Bulgarian | `hr` | Croatian | `pt-PT` | Portuguese (Portugal) |
| `cs` | Czech | `hu` | Hungarian | `ro` | Romanian |
| `da` | Danish | `id` | Indonesian | `ru` | Russian |
| `de` | German | `it` | Italian | `sk` | Slovak |
| `el` | Greek | `ja` | Japanese | `sl` | Slovenian |
| `en` | English | `ko` | Korean | `sr` | Serbian |
| `es` | Spanish | `lt` | Lithuanian | `sv` | Swedish |
| `es-MX` | Spanish (Mexico) | `lv` | Latvian | `th` | Thai |
| `et` | Estonian | `ms` | Malay | `tr` | Turkish |
| `fi` | Finnish | `nl` | Dutch | `uk` | Ukrainian |
| `fr` | French | `no` | Norwegian | `vi` | Vietnamese |
| `he` | Hebrew | `pl` | Polish | `zh-cn` | Chinese (Simplified) |

## Voices

### German

| Voice | Gender | Style |
|---|---|---|
| `Nadja` | Female | Natural, warm (recommended) |
| `Thomas` | Male | Professional, clear |
| `Anna` | Female | Friendly, versatile |
| `Hans` | Male | Neutral, factual |
| `Friedrich` | Male | Formal, authoritative |
| `Anneliese` | Female | Conversational, lively |

### English

| Voice | Gender | Style |
|---|---|---|
| `Emily` | Female | Natural, warm |
| `James` | Male | Professional, clear |

> **Tip:** The full list of available voices can be retrieved via the API. Voice availability varies by language.

## Voice Cloning

Clone any voice from a short audio sample (5–15 seconds).

| Parameter | Type | Required | Description |
|---|---|---|---|
| `voice_sample` | file | **Yes** | Audio file of voice to clone (WAV, MP3, OGG, FLAC, M4A, WebM, AAC). 5–15 seconds, clean audio, max 10 MB |
| `text` | string | **Yes** | Text to speak with the cloned voice |
| `quality` | string | No | `premium` or `ultra` only (basic not supported for cloning) |
| `language` | string | No | Auto-detected from sample if empty |

> **Note:** When using `voice_sample`, do **not** send `voice` — the sample IS the voice.

```bash
curl -X POST "https://api.paperoffice.ai/latest/job/add/paperoffice_voice___tts" \
  -H "Authorization: Bearer $PAPEROFFICE_API_KEY" \
  -F "text=Hello, this is my cloned voice speaking." \
  -F "voice_sample=@my_voice.wav" \
  -F "quality=premium" \
  -F "priority=999"
```

## Multi-Speaker (Inline Tags)

Generate audio with multiple voices in a single request using inline tags.

### Syntax

```
[de|Anneliese] Hallo, ich bin Anneliese.
[en|Emily] And I am Emily, nice to meet you.
[de|Thomas] Und ich bin Thomas.
```

### Key-Value syntax (advanced)

```
[voice:Anneliese lang:de] Hallo zusammen.
[voice:Emily lang:en quality:ultra] This is Emily in ultra quality.
```

### Emotion markers

```
[de|Nadja] (excited) Das ist fantastisch!
[de|Nadja] (whispering) Das ist ein Geheimnis.
```

## Response

```json
{
  "status": "success",
  "result": {
    "status": "completed",
    "audio_url": "https://api-c3.paperoffice.ai:44390/latest/binary_download.php?file=...",
    "audio_duration_seconds": 1.046,
    "voice": "Nadja",
    "language": "de",
    "mime_type": "audio/mpeg",
    "audio_size": 27002,
    "output_mode": "url",
    "text_length": 6,
    "processing_time_seconds": 0.857
  }
}
```

## Output formats

| Format | MIME | Note |
|---|---|---|
| `mp3` | `audio/mpeg` | Default, compressed, smallest size |
| `wav` | `audio/wav` | Lossless, highest quality (requires premium or ultra) |
| `ogg` | `audio/ogg` | Open format, good compression (requires premium or ultra) |

## Tips

- **Synchronous:** `priority=999` (or any `≥ 900`) returns result directly
- **Long texts:** For texts > 5,000 characters, use async processing (`priority=500`)
- **Force language:** Set `language` explicitly to override auto-detection
- **Reproducibility:** Same `text` + `voice` + `temperature=0.1` gives near-identical output
- **Speed control:** `0.9` is ~10% slower (calmer), `1.1` is ~10% faster (energetic)

## See also

- [Speech-to-Text](../stt/) — Transcribe audio to text
- [Translation](../translation/) — Translate text between 170+ languages
