#!/usr/bin/env bash
# PaperOffice AI — PDF in andere Formate konvertieren

api_base="https://api.paperoffice.ai/latest"
api_key="${PAPEROFFICE_API_KEY:?Bitte PAPEROFFICE_API_KEY setzen}"
input_file="${1:?Bitte Dateipfad als Argument übergeben}"
target_format="${2:-docx}"

# PDF hochladen und konvertieren
response=$(curl -s "${api_base}/job/add/workflow" \
  -H "Authorization: Bearer ${api_key}" \
  -F "file_1=@${input_file}" \
  -F "template=pdf_convert" \
  -F "target_format=${target_format}" \
  -F "priority=900")

status=$(echo "${response}" | python3 -c "import sys,json; print(json.load(sys.stdin).get('status',''))")
echo "Status: ${status}"
echo "Zielformat: ${target_format}"

if [ "${status}" != "success" ]; then
  echo "Fehler:"
  echo "${response}" | python3 -m json.tool
  exit 1
fi

# Konvertierte Datei herunterladen
download_url=$(echo "${response}" | python3 -c "
import sys, json
files = json.load(sys.stdin).get('result', {}).get('files', [])
if files: print(files[0])
")

if [ -n "${download_url}" ]; then
  output_name="ergebnis.${target_format}"
  curl -s "${download_url}" \
    -H "Authorization: Bearer ${api_key}" \
    -o "${output_name}"
  echo "Heruntergeladen: ${output_name}"
else
  echo "Fehler: Keine Download-URL erhalten"
  exit 1
fi
