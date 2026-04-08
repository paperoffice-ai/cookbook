#!/usr/bin/env bash
# PaperOffice AI — Health Check (VISITOR, no token required)
curl -s "https://api.paperoffice.ai/latest/health" | python3 -m json.tool
