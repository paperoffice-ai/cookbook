#!/usr/bin/env bash
# PaperOffice AI — Verify device fingerprint
set -euo pipefail

API_KEY="${PAPEROFFICE_API_KEY:?Please set PAPEROFFICE_API_KEY (export PAPEROFFICE_API_KEY=po_sk_xxx)}"
VISITOR_ID="${1:-test_visitor_abc123}"

echo "→ Verifying device: $VISITOR_ID"

curl -s -X POST "https://api.paperoffice.ai/latest/fingerprint/verify" \
  -H "Authorization: Bearer ${API_KEY}" \
  -F "visitorId=${VISITOR_ID}" | python3 -m json.tool
