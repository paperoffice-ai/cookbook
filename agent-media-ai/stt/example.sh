#!/usr/bin/env bash
# ═══════════════════════════════════════════════════════════════
# PaperOffice AI — Speech-to-Text (STT)
# Transkribiert Audio-Dateien in Text
# ═══════════════════════════════════════════════════════════════

set -euo pipefail

API_KEY="${PAPEROFFICE_API_KEY:?Bitte PAPEROFFICE_API_KEY setzen (export PAPEROFFICE_API_KEY=po_sk_xxx)}"
BASE_URL="https://api.paperoffice.ai/latest"

AUDIO_FILE="${1:?Bitte Audio-Datei als erstes Argument übergeben (MP3/WAV/OGG/FLAC/M4A/WEBM)}"
LOCALE="${2:-}"

if [ ! -f "${AUDIO_FILE}" ]; then
  echo "Fehler: Datei '${AUDIO_FILE}' nicht gefunden" >&2
  exit 1
fi

echo "→ STT: Transkribiere '${AUDIO_FILE}'"

# Datei-Key ist "file_1" — NICHT "file"!
CURL_ARGS=(
  -s -X POST "${BASE_URL}/job/add/paperoffice_voice___stt"
  -H "Authorization: Bearer ${API_KEY}"
  -F "file_1=@${AUDIO_FILE}"
  -F "priority=900"
)

if [ -n "${LOCALE}" ]; then
  CURL_ARGS+=(-F "locale=${LOCALE}")
fi

curl "${CURL_ARGS[@]}" | python3 -m json.tool
