# Windsurf — Auto-Classification System

**Tool:** Windsurf IDE | **Output:** Auto-Classification System mit Folder Watch

## Prompt

Kopiere diesen Prompt direkt in Windsurf:

```
Read this API documentation:
https://api.paperoffice.ai/latest/docs/postman

Build a document classifier that:
1. Watches a folder for new PDFs
2. Uses OCR (POST /job/add/workflow, ocr_mode=complete) to extract text
3. Classifies into: invoice, contract, receipt, correspondence
4. Moves files to category subfolders
5. Logs results to classification_log.csv

Use Bearer token for authentication.
Priority=900 for sync response.
```

## Was du bekommst

Ein Klassifikationssystem das:
- Einen Ordner auf neue PDFs überwacht (Watchdog)
- Text via OCR extrahiert
- Dokumente automatisch klassifiziert (Rechnung, Vertrag, Beleg, Korrespondenz)
- Dateien in Kategorie-Unterordner verschiebt
- Ein CSV-Log führt

## Tipps

- Bearer Token erforderlich (`export PAPEROFFICE_API_KEY=po_sk_xxx`)
- `ocr_mode=complete` für Text + Tabellen
- `priority=900` für synchrone Antwort
- Klassifikation kann regelbasiert (Keywords) oder AI-basiert erfolgen
