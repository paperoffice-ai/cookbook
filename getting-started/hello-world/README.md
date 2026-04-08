# Hello World — Health Check

The simplest API call of all: Check whether the PaperOffice AI API is reachable.

## Endpoint

```
GET https://api.paperoffice.ai/latest/health
```

**Authentication:** None — this endpoint is public (VISITOR level).

## How to run

```bash
# Bash
chmod +x example.sh && ./example.sh

# Python
pip install requests
python3 example.py

# Node.js (v18+)
node example.js
```

## Expected response

```json
{
    "success": true,
    "message": "API is healthy",
    "processing_time": "0.002s"
}
```

## What is it for?

This call is perfect as a smoke test in CI/CD pipelines or as a first step to verify connectivity to the API — without any API key.
