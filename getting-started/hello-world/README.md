# Hello World — Health Check

Der einfachste API-Call überhaupt: Prüfe ob die PaperOffice AI API erreichbar ist.

## Endpoint

```
GET https://api.paperoffice.ai/latest/health
```

**Authentifizierung:** Keine — dieser Endpoint ist öffentlich (VISITOR-Level).

## Ausführen

```bash
# Bash
chmod +x example.sh && ./example.sh

# Python
pip install requests
python3 example.py

# Node.js (v18+)
node example.js
```

## Erwartete Antwort

```json
{
    "success": true,
    "message": "API is healthy",
    "processing_time": "0.002s"
}
```

## Wofür?

Dieser Call eignet sich perfekt als Smoke-Test in CI/CD-Pipelines oder als erster Schritt, um die Konnektivität zur API zu verifizieren — ganz ohne API-Key.
