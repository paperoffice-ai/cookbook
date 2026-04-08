#!/usr/bin/env bash
# ═══════════════════════════════════════════════════════════════
# PaperOffice AI — Text-to-Speech Generator
# Bearer Token ERFORDERLICH
# ═══════════════════════════════════════════════════════════════

set -euo pipefail

API_KEY="${PAPEROFFICE_API_KEY:?Bitte PAPEROFFICE_API_KEY setzen (export PAPEROFFICE_API_KEY=po_sk_xxx)}"
TEXT="${1:-Hallo, das ist ein Test der Sprachausgabe.}"
VOICE="${2:-Nadja}"

echo "→ TTS mit Stimme '${VOICE}': ${TEXT}"

curl -s -X POST "https://api.paperoffice.ai/latest/job" \
  -H "Authorization: Bearer ${API_KEY}" \
  -F "text=${TEXT}" \
  -F "voice=${VOICE}" \
  -F "output_format=mp3" \
  -F "output=url" \
  -F "speed=1.0" \
  -F "priority=999" | python3 -m json.tool

# Stimmen: Nadja, Thomas, Anna, Hans (DE) + 100+ internationale Stimmen
