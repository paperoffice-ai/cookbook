#!/usr/bin/env bash
# PaperOffice AI — USt-ID validieren
set -euo pipefail

API_KEY="${PAPEROFFICE_API_KEY:?Bitte PAPEROFFICE_API_KEY setzen (export PAPEROFFICE_API_KEY=po_sk_xxx)}"
VAT_ID="${1:-DE123456789}"

echo "→ Validiere USt-ID: $VAT_ID"

curl -s -X POST "https://api.paperoffice.ai/latest/vat/validate" \
  -H "Authorization: Bearer ${API_KEY}" \
  -F "vat_id=${VAT_ID}" | python3 -m json.tool

echo ""
echo "→ EU-Steuersätze abrufen (GRATIS, kein Token nötig):"
curl -s "https://api.paperoffice.ai/latest/vat/rates" | python3 -m json.tool
