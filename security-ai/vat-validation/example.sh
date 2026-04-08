#!/usr/bin/env bash
# PaperOffice AI — Validate VAT ID
set -euo pipefail

API_KEY="${PAPEROFFICE_API_KEY:?Please set PAPEROFFICE_API_KEY (export PAPEROFFICE_API_KEY=po_sk_xxx)}"
VAT_ID="${1:-DE123456789}"

echo "→ Validating VAT ID: $VAT_ID"

curl -s -X POST "https://api.paperoffice.ai/latest/vat/validate" \
  -H "Authorization: Bearer ${API_KEY}" \
  -F "vat_id=${VAT_ID}" | python3 -m json.tool

echo ""
echo "→ Fetching EU tax rates (FREE, no token required):"
curl -s "https://api.paperoffice.ai/latest/vat/rates" | python3 -m json.tool
