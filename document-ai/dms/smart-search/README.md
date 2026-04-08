# Intelligente Dokumentensuche (Smart Search)

Durchsucht das DMS mit **semantischer KI-Suche**. Die Smart Search versteht Bedeutung und Kontext — nicht nur exakte Schlüsselwörter.

## Endpoint

```
POST https://api.paperoffice.ai/latest/documents/search
```

**Authentifizierung:** Bearer Token (API-Key erforderlich)

## Parameter

| Parameter        | Pflicht | Beschreibung                                        |
|------------------|---------|-----------------------------------------------------|
| `global_search`  | Ja      | Suchbegriff (semantisch + Volltext)                  |
| `workspace_name` | Nein    | Suche auf einen Workspace beschränken                |
| `limit`          | Nein    | Maximale Ergebnisanzahl (Standard: 10)               |
| `offset`         | Nein    | Ergebnisse ab Position (für Paginierung)             |

**Wichtig:** Der Suchparameter heißt `global_search` (nicht `search_query`).

## Ausführen

```bash
export PAPEROFFICE_API_KEY="dein_api_key"

# Bash
bash example.sh "Vertragsbedingungen"
bash example.sh "Rechnung 2026" "Buchhaltung" 5

# Python
pip install requests
python3 example.py "Vertragsbedingungen"
python3 example.py "Rechnung 2026" "Buchhaltung"

# Node.js
node example.js "Vertragsbedingungen"
node example.js "Rechnung 2026" "Buchhaltung" 5
```

## Response-Struktur

```json
{
  "status": "success",
  "results": [
    {
      "id": 1234,
      "filename": "rahmenvertrag_2026.pdf",
      "score": 0.94,
      "snippet": "Die Vertragsbedingungen sehen eine Laufzeit von...",
      "workspace": "Buchhaltung"
    }
  ],
  "total": 42
}
```

## Suchsyntax

Die Smart Search unterstützt verschiedene Suchmodi:

| Modus                | Beispiel                           | Beschreibung                       |
|----------------------|------------------------------------|------------------------------------|
| Semantische Suche    | "Kündigungsfristen im Mietvertrag" | Findet inhaltlich passende Stellen |
| Stichwortsuche       | "IBAN DE89"                        | Exakter Textabgleich               |
| Kombinierte Suche    | "Rechnung über 5000 Euro"          | Semantik + Schlüsselwörter         |

## Semantische Suche

Die KI versteht:

- **Synonyme**: "Gehalt" findet auch "Vergütung", "Lohn", "Entgelt"
- **Kontext**: "Kündigungsfrist" findet auch Passagen über Vertragsbeendigung
- **Mehrsprachig**: Deutsche Suche findet auch englische Dokumente und umgekehrt

## Filter

- **Workspace-Filter**: Suche auf einen bestimmten Workspace einschränken
- **Paginierung**: Mit `limit` und `offset` durch große Ergebnismengen blättern

## Tipps

- Natürliche Fragen liefern oft bessere Ergebnisse als einzelne Stichwörter
- `global_search` kombiniert Volltextsuche mit semantischer Suche automatisch
- Für präzise Ergebnisse: Workspace-Filter nutzen
- Score-Werte > 0.8 gelten als sehr gute Treffer
