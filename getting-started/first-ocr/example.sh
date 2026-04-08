#!/usr/bin/env bash
# PaperOffice AI — Erster OCR-Call (Text-Extraktion)

api_base="https://api.paperoffice.ai/latest"
api_key="${PAPEROFFICE_API_KEY:?Bitte PAPEROFFICE_API_KEY setzen}"
input_file="${1:?Bitte Dateipfad als Argument übergeben}"

response=$(curl -s "${api_base}/job/add/paperoffice_aiocr___generate" \
  -H "Authorization: Bearer ${api_key}" \
  -F "file_1=@${input_file}" \
  -F "ocr_mode=text" \
  -F "priority=900")

# Vollständige Antwort anzeigen
echo "${response}" | python3 -m json.tool

# Extrahierten Text ausgeben
fulltext=$(echo "${response}" | python3 -c "
import sys, json
data = json.load(sys.stdin)
print(data.get('result', {}).get('output', {}).get('summary', {}).get('poaiocr_extracted_fulltext', 'Kein Text extrahiert'))
")
echo ""
echo "--- Extrahierter Text ---"
echo "${fulltext}"
