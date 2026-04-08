# Speech-to-Text (STT)

Transcribes audio files to text. Supports MP3, WAV, OGG, FLAC, M4A and WEBM (max. 25 MB). Automatic language detection or manual language hint.

## Prerequisites

```bash
export PAPEROFFICE_API_KEY=po_sk_xxx
```

## Quick Start

```bash
# cURL
bash example.sh audio.mp3
bash example.sh audio.mp3 de    # with language hint

# Python (requires: pip install requests)
python example.py audio.mp3
python example.py audio.mp3 de

# Node.js 18+
node example.js audio.mp3
node example.js audio.mp3 de
```

## Endpoint

```
POST https://api.paperoffice.ai/latest/job/add/paperoffice_voice___stt
```

## Parameters

| Parameter | Type | Required | Default | Description |
|---|---|---|---|---|
| `file_1` | file | ✅ | — | Audio file (MP3/WAV/OGG/FLAC/M4A/WEBM, max. 25 MB) |
| `priority` | int | — | — | `≥ 900` for synchronous processing |
| `locale` | string | — | auto | Language hint (e.g. `de`, `en`, `fr`) |
| `language` | string | — | auto | Alternative to `locale` |

> **Important:** The file key is `file_1`, **not** `file`!

## Supported Audio Formats

| Format | MIME Type | Note |
|---|---|---|
| MP3 | `audio/mpeg` | Most commonly used |
| WAV | `audio/wav` | Uncompressed, best quality |
| OGG | `audio/ogg` | Compact, good quality |
| FLAC | `audio/flac` | Losslessly compressed |
| M4A | `audio/mp4` | Apple format |
| WEBM | `audio/webm` | Browser recordings |

## Response Example

```json
{
  "status": "success",
  "result": {
    "status": "completed",
    "text": "Dies ist ein kurzer Testtext.",
    "language": "de",
    "audio_duration_seconds": 2.77,
    "quality": "basic"
  }
}
```

## Tips

- **Language hint:** For multilingual audio, `locale` can improve recognition accuracy
- **File size:** Maximum 25 MB per request — split longer recordings beforehand
- **Quality:** The `quality` field indicates the recognition tier used
