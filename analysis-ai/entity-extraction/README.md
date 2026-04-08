# Entity-Extraktion — Named Entity Recognition (NER)

Extrahiert benannte Entitäten (Personen, Organisationen, Orte, Daten, Beträge etc.) aus Texten oder Dokumenten mittels KI-gestützter NER-Analyse.

## Endpoint

```
POST https://api.paperoffice.ai/latest/document_intelligence/entities
```

**Authentifizierung:** Bearer Token

## Parameter

| Parameter | Typ | Pflicht | Beschreibung |
|---|---|---|---|
| `text` | string | ✅* | Zu analysierender Text |
| `file_1` | file | ✅* | Alternativ: Dokument hochladen (PDF, DOCX etc.) |
| `entity_types` | string | ❌ | Komma-separierte Liste: `person`, `organization`, `location`, `date`, `money`, `phone`, `email` |

\* Entweder `text` oder `file_1` muss angegeben werden.

## Ausführen

```bash
export PAPEROFFICE_API_KEY=po_sk_xxx

# Bash
bash example.sh "Die Firma ABC GmbH sitzt in Berlin."

# Python
pip install requests
python3 example.py "Die Firma ABC GmbH sitzt in Berlin."

# Node.js (v18+)
node example.js "Die Firma ABC GmbH sitzt in Berlin."
```

## Erwartete Antwort

```json
{
    "status": "success",
    "entities": [
        {
            "text": "Mustermann GmbH",
            "type": "organization",
            "start": 4,
            "end": 19,
            "confidence": 0.95
        },
        {
            "text": "München",
            "type": "location",
            "start": 33,
            "end": 40,
            "confidence": 0.98
        },
        {
            "text": "15. März 2025",
            "type": "date",
            "start": 48,
            "end": 61,
            "confidence": 0.97
        },
        {
            "text": "250.000 EUR",
            "type": "money",
            "start": 83,
            "end": 94,
            "confidence": 0.96
        }
    ]
}
```

## Unterstützte Entity-Typen

| Typ | Beschreibung | Beispiele |
|---|---|---|
| `person` | Personennamen | Max Mustermann, Dr. Meier |
| `organization` | Firmen, Behörden | Mustermann GmbH, Finanzamt München |
| `location` | Orte, Adressen | München, Hauptstraße 5 |
| `date` | Datumsangaben | 15. März 2025, Q1/2024 |
| `money` | Geldbeträge | 250.000 EUR, 1.500,00 € |
| `phone` | Telefonnummern | +49 89 123456 |
| `email` | E-Mail-Adressen | info@beispiel.de |

## Anwendungsfälle

- **Vertragsanalyse:** Parteien, Beträge und Fristen automatisch aus Verträgen extrahieren
- **Rechnungsverarbeitung:** Lieferanten, Rechnungsnummern und Summen erkennen
- **Compliance:** Personenbezogene Daten in Dokumenten identifizieren (DSGVO)
- **Wissensmanagement:** Entitäten für Knowledge-Graph-Aufbau extrahieren
