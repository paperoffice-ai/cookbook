# Claude — Invoice Pipeline

**Tool:** Claude | **Output:** Komplettes Python-Script mit Bounding Box Verification

## Prompt

Kopiere diesen Prompt direkt in Claude:

```
Read this API documentation:
https://api.paperoffice.ai/latest/docs/postman

Create a Python script that:
1. Takes a folder of invoice PDFs
2. Extracts all fields using POST /job/add/workflow with idp_collection=invoice
3. Returns source_boxes for verification (position data per field)
4. Exports to CSV

Important: Use file_1 for uploads, model=premium.
Handle both sync (priority>=900) and async modes.
```

## Was du bekommst

Claude generiert ein vollständiges Python-Script das:
- Einen Ordner mit Rechnungs-PDFs durchiteriert
- Jede Rechnung via PaperOffice IDP extrahiert
- Source Boxes für visuelles Review bereitstellt
- Ergebnisse als CSV exportiert
- Sync/Async-Modus korrekt handhabt

## Tipps

- Füge `model=premium` hinzu für die beste Extraktionsqualität
- `priority >= 900` = synchrone Antwort, `< 900` = async mit Polling
- Bearer Token erforderlich (`export PAPEROFFICE_API_KEY=po_sk_xxx`)
