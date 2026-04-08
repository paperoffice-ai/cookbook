# IDP mit eigenen Extraktionsfeldern (Custom Fields)

Definiert **eigene Felder** zur gezielten Datenextraktion — für Dokumente, die keine Standard-Collection (invoice, receipt, etc.) abdeckt.

## Endpoint

```
POST https://api.paperoffice.ai/latest/job/add/workflow
```

**Authentifizierung:** Bearer Token (API-Key erforderlich)

## Parameter

| Parameter    | Wert                | Beschreibung                              |
|--------------|---------------------|-------------------------------------------|
| `file_1`     | Datei               | Das zu verarbeitende Dokument             |
| `model`      | `premium`           | Empfohlen für Custom Fields               |
| `idp_fields` | JSON-String         | Array mit Felddefinitionen (siehe unten)  |
| `priority`   | `900`               | Synchrone Verarbeitung (≥900)             |

## idp_fields Syntax

`idp_fields` erwartet ein JSON-Array als String. Jedes Feld hat:

| Eigenschaft   | Typ    | Beschreibung                                  |
|---------------|--------|-----------------------------------------------|
| `name`        | string | Eindeutiger Feldname (snakecase empfohlen)    |
| `type`        | string | `string`, `number`, `date` oder `boolean`     |
| `description` | string | Natürlichsprachige Beschreibung für die KI    |

### Beispiel

```json
[
  {
    "name": "vertragsnummer",
    "type": "string",
    "description": "Vertragsnummer im Dokument"
  },
  {
    "name": "kuendigungsfrist",
    "type": "string",
    "description": "Kündigungsfrist in Monaten oder als Datum"
  },
  {
    "name": "monatlicher_betrag",
    "type": "number",
    "description": "Monatlicher Betrag in Euro"
  },
  {
    "name": "vertragspartner",
    "type": "string",
    "description": "Name des Vertragspartners"
  }
]
```

## Ausführen

```bash
export PAPEROFFICE_API_KEY="dein_api_key"

# Bash
bash example.sh vertrag.pdf

# Python
pip install requests
python3 example.py vertrag.pdf

# Node.js
npm install form-data
node example.js vertrag.pdf
```

## Wann Custom Fields statt Collection?

| Szenario                               | Empfehlung                   |
|----------------------------------------|------------------------------|
| Standardrechnung                       | `idp_collection=invoice`     |
| Kassenbon                              | `idp_collection=receipt`     |
| Vertrag mit speziellen Klauseln        | **Custom Fields**            |
| Technische Spezifikation               | **Custom Fields**            |
| Branchenspezifisches Formular          | **Custom Fields**            |
| Behörden-Bescheid                      | **Custom Fields**            |

## Tipps

- **Beschreibung ist entscheidend**: Je präziser die `description`, desto besser die Extraktion
- Nutze `model=premium` oder `model=ultra` für Custom Fields — `basic` reicht oft nicht
- Kombinierbar: `idp_collection` und `idp_fields` gleichzeitig für Standard + eigene Felder
- Maximal ~50 Custom Fields pro Request empfohlen

## Response-Struktur

```json
{
  "status": "success",
  "job_id": "poai-job_900_...",
  "result": {
    "pages_idp": [{
      "suggested_fields": {
        "vertragsnummer": {
          "type": "string",
          "value": "V-2024-00815",
          "source_boxes_confidence": "high"
        },
        "kuendigungsfrist": {
          "type": "string",
          "value": "3 Monate zum Quartalsende",
          "source_boxes_confidence": "medium"
        }
      }
    }]
  }
}
```
