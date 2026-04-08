#!/usr/bin/env bash
# PaperOffice AI — Webhooks (Subscribe, List, Test)

api_base="https://api.paperoffice.ai/latest"
api_key="${PAPEROFFICE_API_KEY:?Bitte PAPEROFFICE_API_KEY setzen}"
webhook_url="${1:-https://example.com/webhook}"

# Schritt 1: Webhook registrieren
echo ">>> Webhook registrieren..."
subscribe_response=$(curl -s "${api_base}/webhooks/subscribe" \
  -H "Authorization: Bearer ${api_key}" \
  -H "Content-Type: application/json" \
  -d "{
    \"name\": \"mein_erster_webhook\",
    \"url\": \"${webhook_url}\",
    \"events\": [\"job.completed\", \"job.failed\"],
    \"secret\": \"mein_webhook_secret_123\"
  }")

echo "${subscribe_response}" | python3 -m json.tool

# Schritt 2: Alle Webhooks auflisten
echo ""
echo ">>> Webhooks auflisten..."
list_response=$(curl -s "${api_base}/webhooks/list" \
  -H "Authorization: Bearer ${api_key}")

echo "${list_response}" | python3 -m json.tool

# Schritt 3: Test-Event senden
echo ""
echo ">>> Test-Event senden..."
test_response=$(curl -s -X POST "${api_base}/webhooks/test" \
  -H "Authorization: Bearer ${api_key}" \
  -H "Content-Type: application/json" \
  -d "{\"url\": \"${webhook_url}\"}")

echo "${test_response}" | python3 -m json.tool
