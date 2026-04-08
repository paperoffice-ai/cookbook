#!/usr/bin/env bash
# PaperOffice AI — Fake-E-Mail erkennen
set -euo pipefail

API_KEY="${PAPEROFFICE_API_KEY:?Bitte PAPEROFFICE_API_KEY setzen (export PAPEROFFICE_API_KEY=po_sk_xxx)}"
EMAIL="${1:-test@mailinator.com}"

echo "→ Prüfe E-Mail: $EMAIL"

curl -s -X POST "https://api.paperoffice.ai/latest/fakeemail/check" \
  -H "Authorization: Bearer ${API_KEY}" \
  -F "email=${EMAIL}" | python3 -m json.tool
