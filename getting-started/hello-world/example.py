#!/usr/bin/env python3
"""PaperOffice AI — Health Check (VISITOR, no token required)"""
import requests

response = requests.get("https://api.paperoffice.ai/latest/health")
data = response.json()
print(f"Status: {data.get('success')}")
print(f"Message: {data.get('message')}")
print(f"Processing: {data.get('processing_time')}")
