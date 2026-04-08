# Speech-to-Text (STT)

Transcribes audio files to text. Supports MP3, WAV, OGG, FLAC, M4A and WEBM (max 25 MB). Three quality tiers: basic (text only), premium (+ timestamps, subtitles), ultra (+ speaker diarization).

## Endpoint

```
POST https://api.paperoffice.ai/latest/job/add/paperoffice_voice___stt
```

**Authentication:** Bearer Token required

## How to run

```bash
export PAPEROFFICE_API_KEY="your_api_key"

# Bash
chmod +x example.sh && ./example.sh audio.mp3
./example.sh audio.mp3 de   # with language hint

# Python
pip install requests
python3 example.py audio.mp3
python3 example.py audio.mp3 de

# Node.js (v18+)
node example.js audio.mp3
node example.js audio.mp3 de
```

## Parameters

| Parameter | Type | Required | Default | Description |
|---|---|---|---|---|
| `file_1` | file | **Yes** | — | Audio file (max 25 MB). **Key must be `file_1`, not `file`!** |
| `quality` | string | No | `basic` | Quality tier: `basic`, `premium`, `ultra` (see table below) |
| `output_format` | string | No | `json` | `json`, `srt`, `vtt`, `rttm` (see output formats) |
| `locale` | string | No | auto | Language hint (e.g. `de`, `en`, `fr`) — improves accuracy |
| `language` | string | No | auto | Alternative to `locale` (same functionality) |
| `hotwords` | string | No | — | Comma-separated custom vocabulary (premium/ultra only) |
| `min_speakers` | int | No | — | Minimum expected speakers (ultra only) |
| `max_speakers` | int | No | — | Maximum expected speakers (ultra only) |
| `priority` | int | No | `999` | `≥ 900` = synchronous (result inline) |

## Quality tiers

| Tier | Cost | Features | Best for |
|---|---|---|---|
| `basic` | 1 ct/min | Text transcription only | Simple transcription, bulk processing |
| `premium` | 2 ct/min | + Word-level timestamps, SRT/VTT subtitles, hotwords | Subtitle generation, searchable transcripts |
| `ultra` | 3 ct/min | + Speaker diarization, overlap detection, RTTM output | Meetings, interviews, multi-speaker content |

### Feature comparison

| Feature | basic | premium | ultra |
|---|---|---|---|
| Text transcription | ✅ | ✅ | ✅ |
| Language detection | ✅ | ✅ | ✅ |
| Word timestamps | — | ✅ | ✅ |
| SRT/VTT subtitles | — | ✅ | ✅ |
| Custom hotwords | — | ✅ | ✅ |
| Speaker diarization | — | — | ✅ |
| Overlap detection | — | — | ✅ |
| RTTM output | — | — | ✅ |

## Output formats

| Format | Tier required | Description |
|---|---|---|
| `json` | basic+ | Structured JSON with text and metadata (default) |
| `srt` | premium+ | SubRip subtitle format (timecoded) |
| `vtt` | premium+ | WebVTT subtitle format (browser-compatible) |
| `rttm` | ultra | Rich Transcription Time Marked (speaker turns) |

## Supported audio formats

| Format | MIME Type | Note |
|---|---|---|
| MP3 | `audio/mpeg` | Most commonly used |
| WAV | `audio/wav` | Uncompressed, best quality |
| OGG | `audio/ogg` | Compact, good quality |
| FLAC | `audio/flac` | Losslessly compressed |
| M4A | `audio/mp4` | Apple format |
| WEBM | `audio/webm` | Browser recordings |

## Response example (basic)

```json
{
  "status": "success",
  "result": {
    "status": "completed",
    "text": "This is a short test recording.",
    "language": "en",
    "audio_duration_seconds": 2.77,
    "quality": "basic"
  }
}
```

## Response example (premium — with timestamps)

```json
{
  "status": "success",
  "result": {
    "status": "completed",
    "text": "This is a short test recording.",
    "language": "en",
    "audio_duration_seconds": 2.77,
    "quality": "premium",
    "words": [
      { "word": "This", "start": 0.0, "end": 0.3, "confidence": 0.98 },
      { "word": "is", "start": 0.3, "end": 0.5, "confidence": 0.99 },
      { "word": "a", "start": 0.5, "end": 0.6, "confidence": 0.97 }
    ]
  }
}
```

## Hotwords example

Improve recognition for domain-specific terms:

```bash
curl -X POST "https://api.paperoffice.ai/latest/job/add/paperoffice_voice___stt" \
  -H "Authorization: Bearer $PAPEROFFICE_API_KEY" \
  -F "file_1=@meeting.mp3" \
  -F "quality=premium" \
  -F "hotwords=PaperOffice,Kubernetes,GraphQL,OAuth2" \
  -F "priority=999"
```

## Speaker diarization example (ultra)

```bash
curl -X POST "https://api.paperoffice.ai/latest/job/add/paperoffice_voice___stt" \
  -H "Authorization: Bearer $PAPEROFFICE_API_KEY" \
  -F "file_1=@interview.mp3" \
  -F "quality=ultra" \
  -F "min_speakers=2" \
  -F "max_speakers=4" \
  -F "priority=999"
```

## Tips

- **Language hint:** For multilingual audio, `locale` significantly improves accuracy
- **File size:** Maximum 25 MB per request — split longer recordings beforehand
- **Subtitles:** Use `output_format=srt` for video subtitle integration
- **Hotwords:** Add product names, technical terms, or proper nouns to reduce misrecognition
- **Speaker count:** Setting `min_speakers`/`max_speakers` improves diarization quality

## See also

- [Text-to-Speech](../tts/) — Convert text to speech
- [Translation](../translation/) — Translate transcribed text
