# Knowledge Base Suche — Semantische Artikelsuche

Durchsucht Knowledge-Base-Artikel mittels semantischer Suche. Anders als Keyword-Suche findet die semantische Suche auch Treffer, die den gleichen Sinn haben, aber andere Worte verwenden.

## Endpoint

```
POST https://api.paperoffice.ai/latest/knowledge/search
```

**Authentifizierung:** Bearer Token

## Parameter

| Parameter | Typ | Pflicht | Beschreibung |
|---|---|---|---|
| `query` | string | ✅ | Suchanfrage in natürlicher Sprache |
| `kb_id` | int | ❌ | Suche auf eine bestimmte KB einschränken |
| `limit` | int | ❌ | Max. Anzahl Ergebnisse (Standard: 5) |

## Ausführen

```bash
export PAPEROFFICE_API_KEY=po_sk_xxx

# Bash — einfache Suche
bash example.sh "Wie funktioniert OCR?"

# Bash — Suche in bestimmter KB mit Limit
bash example.sh "Wie funktioniert OCR?" 9 3

# Python
pip install requests
python3 example.py "Wie funktioniert OCR?"

# Node.js (v18+)
node example.js "Wie funktioniert OCR?"
```

## Erwartete Antwort

```json
{
    "status": "success",
    "results": [
        {
            "article_id": 1,
            "title": "OCR-Grundlagen",
            "snippet": "Optical Character Recognition (OCR) wandelt Bilder von Text in maschinenlesbaren Text um...",
            "score": 0.92
        },
        {
            "article_id": 5,
            "title": "Dokumentenverarbeitung",
            "snippet": "Die Dokumentenverarbeitung nutzt OCR als ersten Schritt, um Text aus gescannten Dokumenten...",
            "score": 0.78
        }
    ]
}
```

## Scoring

| Score-Bereich | Bedeutung |
|---|---|
| 0.90 – 1.00 | Sehr hohe Relevanz — direkte Treffer |
| 0.70 – 0.89 | Hohe Relevanz — thematisch passend |
| 0.50 – 0.69 | Mittlere Relevanz — verwandtes Thema |
| < 0.50 | Geringe Relevanz — nur entfernt verwandt |

## Semantisch vs. Keyword

| Suchanfrage | Keyword-Suche | Semantische Suche |
|---|---|---|
| „Wie scanne ich Dokumente?" | Findet nur Artikel mit „scanne" oder „Dokumente" | Findet auch Artikel über OCR, Dokumentenverarbeitung, IDP |
| „Rechnung verarbeiten" | Findet nur exakte Wortübereinstimmungen | Findet auch Artikel über Invoice Processing, Belegerfassung |

## Anwendungsfälle

- **Helpdesk-KI:** Passende FAQ-Artikel für Kundenanfragen finden
- **Chatbot:** Kontextrelevante Wissensartikel als Grundlage für Antworten
- **Interne Suche:** Mitarbeitern relevante Dokumentation bereitstellen
- **RAG-Pipeline:** Retrieval-Augmented Generation mit Knowledge-Base-Kontext
