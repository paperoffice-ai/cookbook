#!/usr/bin/env bash
# PaperOffice AI — Geocoding (address → coordinates and vice versa)
set -euo pipefail

API_KEY="${PAPEROFFICE_API_KEY:?Please set PAPEROFFICE_API_KEY (export PAPEROFFICE_API_KEY=po_sk_xxx)}"
ADDRESS="${1:-Alexanderplatz 1, Berlin}"

echo "=== Forward Geocoding: $ADDRESS ==="
curl -s -X POST "https://api.paperoffice.ai/latest/geocoding/forward" \
  -H "Authorization: Bearer ${API_KEY}" \
  -F "address=${ADDRESS}" \
  -F "lang=de" | python3 -m json.tool

echo ""
echo "=== Reverse Geocoding: 52.52, 13.41 ==="
curl -s -X POST "https://api.paperoffice.ai/latest/geocoding/reverse" \
  -H "Authorization: Bearer ${API_KEY}" \
  -F "lat=52.52" \
  -F "lng=13.41" \
  -F "lang=de" | python3 -m json.tool
