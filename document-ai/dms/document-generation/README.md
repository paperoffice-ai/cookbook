# KI-basierte Dokumentenerstellung (Document Generation)

Erstellt Dokumente aus **Templates mit Variablen** — Rechnungen, Verträge, Berichte und mehr. Die KI füllt Platzhalter automatisch und generiert formatierte PDF- oder DOCX-Dateien.

## Endpoint

```
POST https://api.paperoffice.ai/latest/document_generation/generate
```

**Authentifizierung:** Bearer Token (API-Key erforderlich)

## Parameter

| Parameter       | Pflicht | Beschreibung                                    |
|-----------------|---------|-------------------------------------------------|
| `template`      | Ja      | Name des Templates (z.B. "invoice_standard")    |
| `variables`     | Nein    | JSON-Objekt mit Template-Variablen              |
| `output_format` | Nein    | Ausgabeformat: `pdf` (Standard) oder `docx`     |

## Ausführen

```bash
export PAPEROFFICE_API_KEY="dein_api_key"

# Bash
bash example.sh "invoice_standard" pdf

# Python
pip install requests
python3 example.py "invoice_standard" pdf

# Node.js
node example.js "invoice_standard" pdf
```

## Response-Struktur

```json
{
  "status": "success",
  "document": {
    "download_url": "https://api.paperoffice.ai/latest/documents/download/abc123",
    "format": "pdf",
    "pages": 2
  }
}
```

## Template-System

Templates verwenden Platzhalter im Format `{{variable}}`:

```
Sehr geehrte Damen und Herren,

hiermit stellen wir Ihnen für unsere Leistungen folgenden Betrag in Rechnung:

Rechnungsnummer: {{rechnungsnummer}}
Datum:           {{datum}}
Firma:           {{firma}}
Betrag:          {{betrag}} EUR
```

## Variablen

Variablen werden als JSON-Objekt übergeben:

```json
{
  "firma": "Muster GmbH",
  "rechnungsnummer": "2026-042",
  "betrag": "1.250,00",
  "datum": "08.04.2026"
}
```

## Ausgabeformate

| Format | Beschreibung                                |
|--------|---------------------------------------------|
| `pdf`  | PDF-Datei (Standard) — ideal für Versand    |
| `docx` | Word-Dokument — ideal für Nachbearbeitung   |

## Tipps

- **Templates vorab definieren** — wiederverwendbare Vorlagen für häufige Dokumente
- **Variablen validieren** — fehlende Platzhalter werden leer gelassen
- **Download-URL** ist zeitlich begrenzt — direkt nach Generierung herunterladen
- Kombinierbar mit `document-upload/` um generierte Dokumente im DMS zu archivieren
