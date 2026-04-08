#!/usr/bin/env bash
# PaperOffice AI — Mehrere PDFs zu einem Dokument zusammenfügen

api_base="https://api.paperoffice.ai/latest"
api_key="${PAPEROFFICE_API_KEY:?Bitte PAPEROFFICE_API_KEY setzen}"
file_1="${1:?Bitte erste PDF als Argument übergeben}"
file_2="${2:?Bitte zweite PDF als Argument übergeben}"

# PDFs hochladen und zusammenfügen
response=$(curl -s "${api_base}/job/add/workflow" \
  -H "Authorization: Bearer ${api_key}" \
  -F "file_1=@${file_1}" \
  -F "file_2=@${file_2}" \
  -F "template=pdf_merge" \
  -F "output_filename=merged.pdf" \
  -F "priority=900")

status=$(echo "${response}" | python3 -c "import sys,json; print(json.load(sys.stdin).get('status',''))")
echo "Status: ${status}"

if [ "${status}" != "success" ]; then
  echo "Fehler:"
  echo "${response}" | python3 -m json.tool
  exit 1
fi

# Zusammengefügtes PDF herunterladen
download_url=$(echo "${response}" | python3 -c "
import sys, json
files = json.load(sys.stdin).get('result', {}).get('files', [])
if files: print(files[0])
")

if [ -n "${download_url}" ]; then
  curl -s "${download_url}" \
    -H "Authorization: Bearer ${api_key}" \
    -o "merged.pdf"
  echo "Heruntergeladen: merged.pdf"
else
  echo "Fehler: Keine Download-URL erhalten"
  exit 1
fi
