# PDF AI Split — Intelligentes Splitting mit KI-Erkennung

Teilt ein mehrseitiges PDF automatisch in logische Einzeldokumente auf. Die KI erkennt Dokumentgrenzen (z.B. wo eine Rechnung endet und ein Lieferschein beginnt) und benennt die Teildokumente intelligent.

## Endpoint

```
POST https://api.paperoffice.ai/latest/job/add/workflow
```

**Authentifizierung:** Bearer Token (API-Key erforderlich)

## Parameter

| Parameter             | Wert              | Beschreibung                                    |
|-----------------------|-------------------|-------------------------------------------------|
| `file_1`              | Datei             | Das zu splittende PDF                           |
| `template`            | `pdf_ai_split`    | Workflow-Template für KI-Split                  |
| `naming_instruction`  | Text              | Anweisung zur Benennung der Teildokumente       |
| `priority`            | `900`             | Synchrone Verarbeitung (≥900 = sofort)          |

## Ausführen

```bash
export PAPEROFFICE_API_KEY="dein_api_key"

# Bash
chmod +x example.sh && ./example.sh /pfad/zur/datei.pdf

# Python
pip install requests
python3 example.py /pfad/zur/datei.pdf

# Node.js (v18+)
node example.js /pfad/zur/datei.pdf
```

## naming_instruction — Beispiele

| Anweisung | Ergebnis |
|-----------|----------|
| `Benenne nach Dokumenttyp und Datum` | `Rechnung_2024-03-15_Mustermann_GmbH.pdf` |
| `Verwende Rechnungsnummer als Dateiname` | `RE-2024-00142.pdf` |
| `Benenne nach Absender und Typ` | `Telekom_Rechnung.pdf` |
| `Nummeriere fortlaufend mit Präfix SCAN` | `SCAN_001.pdf` |

## Response-Struktur

```json
{
  "status": "success",
  "job_id": "poai-job_900_...",
  "operation": "pdf_ai_split",
  "result": {
    "documents": [
      {
        "suggested_filename": "Rechnung_2024-03-15_Mustermann_GmbH.pdf",
        "document_type": "Rechnung",
        "page_range": "1-3",
        "pages": 3,
        "date": "2024-03-15",
        "sender": "Mustermann GmbH",
        "reasoning": "Das Dokument ist eine Rechnung der Mustermann GmbH..."
      }
    ],
    "files": [
      "https://api.paperoffice.ai/latest/job/download/ZBVXGX9A..."
    ],
    "duration_ms": 4610
  }
}
```

## Download der Teildokumente

Die Download-URLs stehen in `result.files[]` — eine URL pro Dokument in `result.documents[]`:

```bash
curl -s "https://api.paperoffice.ai/latest/job/download/ZBVXGX9A..." \
  -H "Authorization: Bearer ${PAPEROFFICE_API_KEY}" \
  -o "Rechnung_2024-03-15.pdf"
```

## Wichtige Felder pro Dokument

| Feld                  | Beschreibung                                          |
|-----------------------|-------------------------------------------------------|
| `suggested_filename`  | KI-generierter Dateiname basierend auf naming_instruction |
| `document_type`       | Erkannter Dokumenttyp (Rechnung, Vertrag, etc.)       |
| `page_range`          | Seitenbereich im Originaldokument                     |
| `pages`               | Anzahl Seiten                                         |
| `date`                | Erkanntes Dokumentdatum                               |
| `sender`              | Erkannter Absender/Aussteller                         |
| `reasoning`           | KI-Begründung für die Klassifizierung                 |

## Typische Anwendungsfälle

- **Posteingang digitalisieren** — Gescannte Stapel in Einzeldokumente aufteilen
- **Rechnungsverarbeitung** — Sammel-PDFs vom Lieferanten in einzelne Rechnungen trennen
- **Vertragsmanagement** — Mehrseitige Vertragspakete in Einzelverträge splitten
- **Archivierung** — Große Scan-Batches automatisch kategorisieren und benennen

## Siehe auch

- [PDF Merge](../merge/) — Mehrere PDFs zusammenfügen
- [PDF Convert](../convert/) — PDF in andere Formate konvertieren
- [PDF Anonymize](../anonymize/) — DSGVO-konforme Anonymisierung
