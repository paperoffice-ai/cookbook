# AI PDF Split — bis 3000 Seiten

Splittet Sammel-PDFs automatisch anhand AI-erkannter Dokumentgrenzen. Funktioniert mit PDFs bis zu **3000 Seiten**.

## Voraussetzungen

```bash
export PAPEROFFICE_API_KEY=po_sk_xxx
```

## Quick Start

```bash
# cURL
bash example.sh sammel_dokument.pdf

# Python
pip install requests
python example.py sammel_dokument.pdf

# Node.js
npm install form-data
node example.js sammel_dokument.pdf
```

## Wie es funktioniert

1. PDF hochladen
2. AI erkennt wo ein Dokument aufhört und das nächste beginnt
3. Für jedes Teildokument: vorgeschlagener Dateiname + Seitenbereich
4. `naming_instruction` steuert das Namensschema (z.B. `Dokumenttyp_Datum_Absender`)

## API-Details

| Parameter | Wert | Beschreibung |
|---|---|---|
| `Authorization` | `Bearer po_sk_xxx` | **Erforderlich** |
| `file` | PDF | Sammel-PDF (bis 3000 Seiten) |
| `template` | `pdf_ai_split` | AI-Split aktivieren |
| `naming_instruction` | Freitext | Schema für Dateinamen |
| `locale` | `de_DE` | Sprache für Dokumenttyp-Erkennung |
| `priority` | `900` | Synchrone Antwort (≥900) |
