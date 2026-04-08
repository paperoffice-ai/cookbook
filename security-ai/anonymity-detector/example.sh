#!/usr/bin/env bash
# PaperOffice AI — VPN/Proxy/Tor detection
set -euo pipefail

API_KEY="${PAPEROFFICE_API_KEY:?Please set PAPEROFFICE_API_KEY (export PAPEROFFICE_API_KEY=po_sk_xxx)}"
IP_ADDR="${1:-}"

echo "→ Anonymity check${IP_ADDR:+ for: $IP_ADDR}"

CMD=(curl -s -X POST "https://api.paperoffice.ai/latest/ip2location/vpn"
  -H "Authorization: Bearer ${API_KEY}")

if [ -n "$IP_ADDR" ]; then
  CMD+=(-F "ip=${IP_ADDR}")
fi

"${CMD[@]}" | python3 -m json.tool
