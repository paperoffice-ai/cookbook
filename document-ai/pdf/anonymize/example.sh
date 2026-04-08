#!/usr/bin/env bash
# PaperOffice AI — DSGVO-konforme Anonymisierung von PDF-Dokumenten

api_base="https://api.paperoffice.ai/latest"
api_key="${PAPEROFFICE_API_KEY:?Bitte PAPEROFFICE_API_KEY setzen}"
input_file="${1:?Bitte Dateipfad als Argument übergeben}"

# PDF hochladen und anonymisieren
response=$(curl -s "${api_base}/job/add/workflow" \
  -H "Authorization: Bearer ${api_key}" \
  -F "file_1=@${input_file}" \
  -F "template=pdf_anonymize" \
  -F "priority=900")

status=$(echo "${response}" | python3 -c "import sys,json; print(json.load(sys.stdin).get('status',''))")
echo "Status: ${status}"

if [ "${status}" != "success" ]; then
  echo "Fehler:"
  echo "${response}" | python3 -m json.tool
  exit 1
fi

# Anonymisierte PDF herunterladen
download_url=$(echo "${response}" | python3 -c "
import sys, json
files = json.load(sys.stdin).get('result', {}).get('files', [])
if files: print(files[0])
")

if [ -n "${download_url}" ]; then
  curl -s "${download_url}" \
    -H "Authorization: Bearer ${api_key}" \
    -o "anonymisiert.pdf"
  echo "Heruntergeladen: anonymisiert.pdf"
else
  echo "Fehler: Keine Download-URL erhalten"
  exit 1
fi
