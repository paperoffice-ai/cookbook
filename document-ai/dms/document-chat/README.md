# Chat mit Dokumenten (Document Intelligence)

Stellt Fragen an ein hochgeladenes Dokument und erhält **KI-generierte Antworten mit Quellenangaben**. Basiert auf RAG (Retrieval-Augmented Generation) — die KI liest das Dokument und antwortet präzise auf Basis des Inhalts.

## Endpoint

```
POST https://api.paperoffice.ai/latest/document_intelligence/chat
```

**Authentifizierung:** Bearer Token (API-Key erforderlich)

## Parameter

| Parameter        | Pflicht | Beschreibung                                      |
|------------------|---------|---------------------------------------------------|
| `document_id`    | Ja      | ID des Dokuments (aus Upload-Response)             |
| `question`       | Ja      | Frage an das Dokument (natürliche Sprache)         |
| `context_window` | Nein    | Kontextfenster-Größe (mehr = breiterer Kontext)    |

## Ausführen

```bash
export PAPEROFFICE_API_KEY="dein_api_key"

# Bash — einzelne Frage
bash example.sh 1234 "Was ist die Kündigungsfrist?"

# Python — einzelne Frage
pip install requests
python3 example.py 1234 "Was ist die Kündigungsfrist?"

# Python — interaktiver Modus
python3 example.py 1234

# Node.js
node example.js 1234 "Was ist die Kündigungsfrist?"
```

## Response-Struktur

```json
{
  "status": "success",
  "answer": "Die Kündigungsfrist beträgt 3 Monate zum Quartalsende gemäß §5 Abs. 2 des Vertrags.",
  "sources": [
    {
      "page": 3,
      "text": "Die Vertragslaufzeit beträgt 12 Monate. Die Kündigungsfrist beträgt 3 Monate...",
      "confidence": "high"
    }
  ]
}
```

## Document Intelligence (RAG-Konzept)

Die Document Intelligence kombiniert zwei Schritte:

1. **Retrieval** — Die relevantesten Passagen im Dokument werden identifiziert
2. **Generation** — Die KI formuliert eine Antwort basierend auf den gefundenen Passagen

### Vorteile gegenüber einfacher Suche

| Eigenschaft         | Suche              | Document Chat                |
|---------------------|--------------------|------------------------------|
| Ausgabe             | Textfragmente      | Formulierte Antwort          |
| Quellenangaben      | Nein               | Ja (Seite, Text, Konfidenz)  |
| Zusammenfassung     | Nein               | Ja                           |
| Folgefragen         | Nein               | Ja (Kontext bleibt erhalten) |

## Quellenangaben

Jede Antwort enthält `sources` mit:

| Feld          | Beschreibung                               |
|---------------|--------------------------------------------|
| `page`        | Seitennummer im Dokument                   |
| `text`        | Relevanter Textausschnitt                  |
| `confidence`  | Konfidenz: `high`, `medium`, `low`         |

## Tipps

- **Präzise Fragen** liefern bessere Antworten als vage Anfragen
- **Interaktiver Modus** (Python) erlaubt Folgefragen zum selben Dokument
- **context_window** erhöhen für Fragen, die Kontext über mehrere Seiten benötigen
- Dokument muss vorher über `document-upload/` hochgeladen worden sein
- Funktioniert mit PDF, DOCX, Bildern und allen unterstützten Formaten
