#!/usr/bin/env bash
# PaperOffice AI — Query IP geolocation
set -euo pipefail

API_KEY="${PAPEROFFICE_API_KEY:?Please set PAPEROFFICE_API_KEY (export PAPEROFFICE_API_KEY=po_ut_xxx)}"
IP_ADDR="${1:-}"

echo "→ Querying geolocation${IP_ADDR:+ for: $IP_ADDR}"

CMD=(curl -s -X POST "https://api.paperoffice.ai/latest/ip2location/full"
  -H "Authorization: Bearer ${API_KEY}"
  -F "locale=de")

if [ -n "$IP_ADDR" ]; then
  CMD+=(-F "ip=${IP_ADDR}")
fi

"${CMD[@]}" | python3 -m json.tool
