#!/usr/bin/env bash
# PaperOffice AI — IP-Geolocation abfragen
set -euo pipefail

API_KEY="${PAPEROFFICE_API_KEY:?Bitte PAPEROFFICE_API_KEY setzen (export PAPEROFFICE_API_KEY=po_sk_xxx)}"
IP_ADDR="${1:-}"

echo "→ Geolocation abfragen${IP_ADDR:+ für: $IP_ADDR}"

CMD=(curl -s -X POST "https://api.paperoffice.ai/latest/ip2location/full"
  -H "Authorization: Bearer ${API_KEY}"
  -F "locale=de")

if [ -n "$IP_ADDR" ]; then
  CMD+=(-F "ip=${IP_ADDR}")
fi

"${CMD[@]}" | python3 -m json.tool
