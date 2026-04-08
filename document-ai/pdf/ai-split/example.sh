#!/usr/bin/env bash
# PaperOffice AI — Intelligentes PDF-Splitting mit KI-Erkennung

api_base="https://api.paperoffice.ai/latest"
api_key="${PAPEROFFICE_API_KEY:?Bitte PAPEROFFICE_API_KEY setzen}"
input_file="${1:?Bitte Dateipfad als Argument übergeben}"

# PDF hochladen und KI-basiert splitten
response=$(curl -s "${api_base}/job/add/workflow" \
  -H "Authorization: Bearer ${api_key}" \
  -F "file_1=@${input_file}" \
  -F "template=pdf_ai_split" \
  -F "naming_instruction=Benenne nach Dokumenttyp und Datum" \
  -F "priority=900")

status=$(echo "${response}" | python3 -c "import sys,json; print(json.load(sys.stdin).get('status',''))")
echo "Status: ${status}"

if [ "${status}" != "success" ]; then
  echo "Fehler:"
  echo "${response}" | python3 -m json.tool
  exit 1
fi

# Gesplittete Dokumente auflisten
echo ""
echo "--- Gesplittete Dokumente ---"
echo "${response}" | python3 -c "
import sys, json
data = json.load(sys.stdin)
docs = data.get('result', {}).get('documents', [])
files = data.get('result', {}).get('files', [])
print(f'Anzahl Teildokumente: {len(docs)}')
print()
for i, doc in enumerate(docs):
    print(f'  [{i+1}] {doc.get(\"suggested_filename\", \"unbekannt\")}')
    print(f'      Typ:    {doc.get(\"document_type\", \"?\")}')
    print(f'      Seiten: {doc.get(\"page_range\", \"?\")}')
    print(f'      Datum:  {doc.get(\"date\", \"?\")}')
    print(f'      Grund:  {doc.get(\"reasoning\", \"\")}')
    if i < len(files):
        print(f'      URL:    {files[i]}')
    print()
"

# Erstes Teildokument herunterladen
download_url=$(echo "${response}" | python3 -c "
import sys, json
files = json.load(sys.stdin).get('result', {}).get('files', [])
if files: print(files[0])
")

filename=$(echo "${response}" | python3 -c "
import sys, json
docs = json.load(sys.stdin).get('result', {}).get('documents', [])
if docs: print(docs[0].get('suggested_filename', 'teil_1.pdf'))
")

if [ -n "${download_url}" ]; then
  curl -s "${download_url}" \
    -H "Authorization: Bearer ${api_key}" \
    -o "${filename}"
  echo "Heruntergeladen: ${filename}"
fi
