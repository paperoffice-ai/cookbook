#!/usr/bin/env bash
# PaperOffice AI — Device Fingerprint verifizieren
set -euo pipefail

API_KEY="${PAPEROFFICE_API_KEY:?Bitte PAPEROFFICE_API_KEY setzen (export PAPEROFFICE_API_KEY=po_sk_xxx)}"
VISITOR_ID="${1:-test_visitor_abc123}"

echo "→ Verifiziere Gerät: $VISITOR_ID"

curl -s -X POST "https://api.paperoffice.ai/latest/fingerprint/verify" \
  -H "Authorization: Bearer ${API_KEY}" \
  -F "visitorId=${VISITOR_ID}" | python3 -m json.tool
