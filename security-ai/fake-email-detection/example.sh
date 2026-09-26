#!/usr/bin/env bash
# PaperOffice AI — Detect fake email
set -euo pipefail

API_KEY="${PAPEROFFICE_API_KEY:?Please set PAPEROFFICE_API_KEY (export PAPEROFFICE_API_KEY=po_ut_xxx)}"
EMAIL="${1:-test@mailinator.com}"

echo "→ Checking email: $EMAIL"

curl -s -X POST "https://api.paperoffice.ai/latest/fakeemail/check" \
  -H "Authorization: Bearer ${API_KEY}" \
  -F "email=${EMAIL}" | python3 -m json.tool
