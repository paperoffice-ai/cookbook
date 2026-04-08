#!/usr/bin/env bash
# ═══════════════════════════════════════════════════════════════
# PaperOffice AI — Text Translation
# Translates text between 100+ languages (3 quality tiers)
# ═══════════════════════════════════════════════════════════════

set -euo pipefail

API_KEY="${PAPEROFFICE_API_KEY:?Please set PAPEROFFICE_API_KEY (export PAPEROFFICE_API_KEY=po_sk_xxx)}"
BASE_URL="https://api.paperoffice.ai/latest"

TEXT="${1:-Hello World}"
TARGET_LANG="${2:-de}"
SOURCE_LANG="${3:-auto}"
TIER="${4:-premium}"

echo "→ Translating: '${TEXT}'"
echo "  ${SOURCE_LANG} → ${TARGET_LANG} (Tier: ${TIER})"

curl -s -X POST "${BASE_URL}/translate/text" \
  -H "Authorization: Bearer ${API_KEY}" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "text=${TEXT}" \
  -d "target_language=${TARGET_LANG}" \
  -d "source_language=${SOURCE_LANG}" \
  -d "tier=${TIER}" | python3 -m json.tool
