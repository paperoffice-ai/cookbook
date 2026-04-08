# Speech-to-Text (STT)

Transkribiert Audio-Dateien in Text. Unterstützt MP3, WAV, OGG, FLAC, M4A und WEBM (max. 25 MB). Automatische Spracherkennung oder manueller Sprach-Hint.

## Voraussetzungen

```bash
export PAPEROFFICE_API_KEY=po_sk_xxx
```

## Quick Start

```bash
# cURL
bash example.sh audio.mp3
bash example.sh audio.mp3 de    # mit Sprach-Hint

# Python (benötigt: pip install requests)
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

## Parameter

| Parameter | Typ | Pflicht | Default | Beschreibung |
|---|---|---|---|---|
| `file_1` | file | ✅ | — | Audio-Datei (MP3/WAV/OGG/FLAC/M4A/WEBM, max. 25 MB) |
| `priority` | int | — | — | `≥ 900` für synchrone Verarbeitung |
| `locale` | string | — | auto | Sprach-Hint (z.B. `de`, `en`, `fr`) |
| `language` | string | — | auto | Alternative zu `locale` |

> **Wichtig:** Der Datei-Key ist `file_1`, **nicht** `file`!

## Unterstützte Audio-Formate

| Format | MIME-Type | Hinweis |
|---|---|---|
| MP3 | `audio/mpeg` | Am häufigsten verwendet |
| WAV | `audio/wav` | Unkomprimiert, beste Qualität |
| OGG | `audio/ogg` | Kompakt, gute Qualität |
| FLAC | `audio/flac` | Verlustfrei komprimiert |
| M4A | `audio/mp4` | Apple-Format |
| WEBM | `audio/webm` | Browser-Aufnahmen |

## Response-Beispiel

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

## Tipps

- **Sprach-Hint:** Bei mehrsprachigen Audios kann `locale` die Erkennungsgenauigkeit verbessern
- **Dateigröße:** Maximal 25 MB pro Request — längere Aufnahmen vorher splitten
- **Qualität:** Das Feld `quality` zeigt die verwendete Erkennungsstufe an
