#!/usr/bin/env bash
# PaperOffice AI — Async Job-Polling (Submit → Poll → Ergebnis)

api_base="https://api.paperoffice.ai/latest"
api_key="${PAPEROFFICE_API_KEY:?Bitte PAPEROFFICE_API_KEY setzen}"
input_file="${1:?Bitte Dateipfad als Argument übergeben}"

# Schritt 1: Job einreichen (priority=500 → async)
echo ">>> Job einreichen..."
submit_response=$(curl -s "${api_base}/job/add/paperoffice_aiocr___generate" \
  -H "Authorization: Bearer ${api_key}" \
  -F "file_1=@${input_file}" \
  -F "ocr_mode=text" \
  -F "priority=500")

job_id=$(echo "${submit_response}" | python3 -c "
import sys, json
data = json.load(sys.stdin)
print(data.get('job_id', ''))
")

if [ -z "${job_id}" ]; then
  echo "Fehler: Keine job_id erhalten"
  echo "${submit_response}" | python3 -m json.tool
  exit 1
fi

echo "Job eingereicht: ${job_id}"

# Schritt 2: Status pollen bis fertig
echo ">>> Warte auf Ergebnis..."
max_attempts=30
attempt=0

while [ ${attempt} -lt ${max_attempts} ]; do
  attempt=$((attempt + 1))
  sleep 2

  poll_response=$(curl -s "${api_base}/job/get/${job_id}" \
    -H "Authorization: Bearer ${api_key}")

  status=$(echo "${poll_response}" | python3 -c "
import sys, json
data = json.load(sys.stdin)
print(data.get('status', 'unknown'))
")

  echo "  Versuch ${attempt}/${max_attempts}: ${status}"

  if [ "${status}" = "completed" ]; then
    echo ""
    echo "--- Ergebnis ---"
    echo "${poll_response}" | python3 -m json.tool
    exit 0
  fi

  if [ "${status}" = "failed" ] || [ "${status}" = "error" ]; then
    echo "Job fehlgeschlagen!"
    echo "${poll_response}" | python3 -m json.tool
    exit 1
  fi
done

echo "Timeout: Job nach ${max_attempts} Versuchen nicht fertig"
exit 1
