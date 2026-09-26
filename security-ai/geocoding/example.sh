#!/usr/bin/env bash
# PaperOffice AI — Geocoding (address → coordinates and vice versa)
set -euo pipefail

API_KEY="${PAPEROFFICE_API_KEY:?Please set PAPEROFFICE_API_KEY (export PAPEROFFICE_API_KEY=po_ut_xxx)}"
ADDRESS="${1:-Berlin, Germany}"

echo "=== Forward Geocoding: $ADDRESS ==="
curl -s -X POST "https://api.paperoffice.ai/latest/geocoding/forward" \
  -H "Authorization: Bearer ${API_KEY}" \
  -F "address=${ADDRESS}" \
  -F "lang=en" | python3 -m json.tool

echo ""
echo "=== Reverse Geocoding: 52.5174, 13.3951 ==="
curl -s -X POST "https://api.paperoffice.ai/latest/geocoding/reverse" \
  -H "Authorization: Bearer ${API_KEY}" \
  -F "lat=52.5174" \
  -F "lng=13.3951" \
  -F "lang=en" | python3 -m json.tool
