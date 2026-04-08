#!/usr/bin/env bash
# ═══════════════════════════════════════════════════════════════
# PaperOffice AI — Textübersetzung
# Übersetzt Texte zwischen 100+ Sprachen (3 Qualitätsstufen)
# ═══════════════════════════════════════════════════════════════

set -euo pipefail

API_KEY="${PAPEROFFICE_API_KEY:?Bitte PAPEROFFICE_API_KEY setzen (export PAPEROFFICE_API_KEY=po_sk_xxx)}"
BASE_URL="https://api.paperoffice.ai/latest"

TEXT="${1:-Hello World}"
TARGET_LANG="${2:-de}"
SOURCE_LANG="${3:-auto}"
TIER="${4:-premium}"

echo "→ Übersetze: '${TEXT}'"
echo "  ${SOURCE_LANG} → ${TARGET_LANG} (Tier: ${TIER})"

curl -s -X POST "${BASE_URL}/translate/text" \
  -H "Authorization: Bearer ${API_KEY}" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "text=${TEXT}" \
  -d "target_language=${TARGET_LANG}" \
  -d "source_language=${SOURCE_LANG}" \
  -d "tier=${TIER}" | python3 -m json.tool
