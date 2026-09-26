#!/usr/bin/env bash
# ═══════════════════════════════════════════════════════════════
# PaperOffice AI — Speech-to-Text (STT)
# Transcribes audio files to text
# ═══════════════════════════════════════════════════════════════

set -euo pipefail

API_KEY="${PAPEROFFICE_API_KEY:?Please set PAPEROFFICE_API_KEY (export PAPEROFFICE_API_KEY=po_ut_xxx)}"
BASE_URL="https://api.paperoffice.ai/latest"

AUDIO_FILE="${1:?Please pass audio file as first argument (MP3/WAV/OGG/FLAC/M4A/WEBM)}"
LOCALE="${2:-}"

if [ ! -f "${AUDIO_FILE}" ]; then
  echo "Error: File '${AUDIO_FILE}' not found" >&2
  exit 1
fi

echo "→ STT: Transcribing '${AUDIO_FILE}'"

# File key is "file_1" — NOT "file"!
CURL_ARGS=(
  -s -X POST "${BASE_URL}/job/add/paperoffice_voice___stt"
  -H "Authorization: Bearer ${API_KEY}"
  -F "file_1=@${AUDIO_FILE}"
  -F "processing_lane=instant"
)

if [ -n "${LOCALE}" ]; then
  CURL_ARGS+=(-F "locale=${LOCALE}")
fi

curl "${CURL_ARGS[@]}" | python3 -m json.tool
