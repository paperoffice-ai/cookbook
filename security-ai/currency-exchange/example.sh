#!/usr/bin/env bash
# PaperOffice AI — Wechselkurse abfragen
set -euo pipefail

FROM="${1:-EUR}"
TO="${2:-}"
AMOUNT="${3:-100}"

echo "→ Wechselkurse: ${AMOUNT} ${FROM}${TO:+ → $TO}"

API_KEY="${PAPEROFFICE_API_KEY:-}"

CMD=(curl -s -X POST "https://api.paperoffice.ai/latest/currency_exchange/get_rates"
  -F "from=${FROM}"
  -F "amount=${AMOUNT}")

if [ -n "$API_KEY" ]; then
  CMD+=(-H "Authorization: Bearer ${API_KEY}")
fi
if [ -n "$TO" ]; then
  CMD+=(-F "to=${TO}")
fi

"${CMD[@]}" | python3 -m json.tool
