#!/usr/bin/env bash
# ═══════════════════════════════════════════════════════════════
# PaperOffice AI — Text-to-Speech (TTS)
# Wandelt Text in natürliche Sprache um (100+ Stimmen)
# ═══════════════════════════════════════════════════════════════

set -euo pipefail

API_KEY="${PAPEROFFICE_API_KEY:?Bitte PAPEROFFICE_API_KEY setzen (export PAPEROFFICE_API_KEY=po_sk_xxx)}"
BASE_URL="https://api.paperoffice.ai/latest"

TEXT="${1:-Hallo, das ist ein Test der PaperOffice Sprachsynthese.}"
VOICE="${2:-Nadja}"
FORMAT="${3:-mp3}"

echo "→ TTS: Stimme '${VOICE}', Format '${FORMAT}'"
echo "  Text: ${TEXT}"

curl -s -X POST "${BASE_URL}/job/add/paperoffice_voice___tts" \
  -H "Authorization: Bearer ${API_KEY}" \
  -F "text=${TEXT}" \
  -F "voice=${VOICE}" \
  -F "output_format=${FORMAT}" \
  -F "output=url" \
  -F "speed=1.0" \
  -F "priority=900" | python3 -m json.tool
