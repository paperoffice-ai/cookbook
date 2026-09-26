#!/usr/bin/env bash
# PaperOffice AI — Fetch weather data (FREE, costs no credits!)
set -euo pipefail

API_KEY="${PAPEROFFICE_API_KEY:?Please set PAPEROFFICE_API_KEY (export PAPEROFFICE_API_KEY=po_ut_xxx)}"
LAT="${1:-52.52}"
LON="${2:-13.41}"
LANG="${3:-de}"

echo "→ Weather for coordinates: $LAT, $LON"

curl -s -G "https://api.paperoffice.ai/latest/weather" \
  -H "Authorization: Bearer ${API_KEY}" \
  --data-urlencode "lat=${LAT}" \
  --data-urlencode "lon=${LON}" \
  --data-urlencode "lang=${LANG}" | python3 -m json.tool
