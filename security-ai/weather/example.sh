#!/usr/bin/env bash
# PaperOffice AI — Wetterdaten abrufen (GRATIS, kostet keine Credits!)
set -euo pipefail

API_KEY="${PAPEROFFICE_API_KEY:?Bitte PAPEROFFICE_API_KEY setzen (export PAPEROFFICE_API_KEY=po_sk_xxx)}"
LAT="${1:-52.52}"
LON="${2:-13.41}"
LOCALE="${3:-de}"

echo "→ Wetter für Koordinaten: $LAT, $LON"

curl -s -X POST "https://api.paperoffice.ai/latest/location2weather" \
  -H "Authorization: Bearer ${API_KEY}" \
  -F "lat=${LAT}" \
  -F "lon=${LON}" \
  -F "locale=${LOCALE}" | python3 -m json.tool
