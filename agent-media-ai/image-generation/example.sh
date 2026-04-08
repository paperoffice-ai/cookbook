#!/usr/bin/env bash
# ═══════════════════════════════════════════════════════════════
# PaperOffice AI — Bildgenerierung
# Erzeugt Bilder aus Text-Prompts (bis 2048×2048)
# ═══════════════════════════════════════════════════════════════

set -euo pipefail

API_KEY="${PAPEROFFICE_API_KEY:?Bitte PAPEROFFICE_API_KEY setzen (export PAPEROFFICE_API_KEY=po_sk_xxx)}"
BASE_URL="https://api.paperoffice.ai/latest"

PROMPT="${1:-A futuristic cityscape at sunset with flying cars}"
MODEL="${2:-premium}"
NUM_IMAGES="${3:-1}"

echo "→ Bildgenerierung: Modell '${MODEL}', ${NUM_IMAGES} Bild(er)"
echo "  Prompt: ${PROMPT}"

curl -s -X POST "${BASE_URL}/job/add/paperoffice_imagestudio___generate" \
  -H "Authorization: Bearer ${API_KEY}" \
  -F "prompt=${PROMPT}" \
  -F "model=${MODEL}" \
  -F "num_images=${NUM_IMAGES}" \
  -F "output=url" \
  -F "precompile_prompt=true" \
  -F "seed=-1" \
  -F "steps=15" \
  -F "guidance_scale=4.0" \
  -F "priority=900" | python3 -m json.tool
