# DSGVO Anonymisierung (PII Preview)

Erkennt personenbezogene Daten (PII) in Dokumenten und zeigt deren Positionen — als Preview vor der eigentlichen Schwärzung.

## Voraussetzungen

```bash
export PAPEROFFICE_API_KEY=po_sk_xxx
```

## Quick Start

```bash
# cURL
bash example.sh vertrag.pdf

# Python
pip install requests
python example.py vertrag.pdf

# Node.js
npm install form-data
node example.js vertrag.pdf
```

## Kategorien

| Kategorie | Erkennt |
|---|---|
| `all` | Alle PII-Typen |
| `names` | Personennamen |
| `addresses` | Adressen |
| `iban` | IBAN-Nummern |
| `phone` | Telefonnummern |
| `email` | E-Mail-Adressen |

Kombinierbar als Kommaliste: `names,addresses,iban`

## Whitelist

Mit `whitelist` können Begriffe von der Schwärzung ausgenommen werden (z.B. Firmenname).

## API-Details

| Parameter | Wert | Beschreibung |
|---|---|---|
| `Authorization` | `Bearer po_sk_xxx` | **Erforderlich** |
| `file` | PDF/Bild | Hochzuladende Datei |
| `template` | `document_anonymize_preview` | PII-Preview-Modus |
| `redact_categories` | `all` | Welche PII-Typen erkennen |
| `whitelist` | Freitext | Begriffe ausnehmen |
| `priority` | `900` | Synchrone Antwort (≥900) |
