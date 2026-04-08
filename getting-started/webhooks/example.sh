#!/usr/bin/env bash
# PaperOffice AI — Webhooks (Subscribe, List, Test)

api_base="https://api.paperoffice.ai/latest"
api_key="${PAPEROFFICE_API_KEY:?Please set PAPEROFFICE_API_KEY}"
webhook_url="${1:-https://example.com/webhook}"

# Step 1: Register webhook
echo ">>> Registering webhook..."
subscribe_response=$(curl -s "${api_base}/webhooks/subscribe" \
  -H "Authorization: Bearer ${api_key}" \
  -H "Content-Type: application/json" \
  -d "{
    \"name\": \"my_first_webhook\",
    \"url\": \"${webhook_url}\",
    \"events\": [\"job.completed\", \"job.failed\"],
    \"secret\": \"my_webhook_secret_123\"
  }")

echo "${subscribe_response}" | python3 -m json.tool

# Step 2: List all webhooks
echo ""
echo ">>> Listing webhooks..."
list_response=$(curl -s "${api_base}/webhooks/list" \
  -H "Authorization: Bearer ${api_key}")

echo "${list_response}" | python3 -m json.tool

# Step 3: Send test event
echo ""
echo ">>> Sending test event..."
test_response=$(curl -s -X POST "${api_base}/webhooks/test" \
  -H "Authorization: Bearer ${api_key}" \
  -H "Content-Type: application/json" \
  -d "{\"url\": \"${webhook_url}\"}")

echo "${test_response}" | python3 -m json.tool
