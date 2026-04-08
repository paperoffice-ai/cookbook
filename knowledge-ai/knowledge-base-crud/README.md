# Knowledge Base — CRUD-Operationen

Erstellen, lesen, aktualisieren und löschen von Knowledge Bases und deren Artikeln. Eine Knowledge Base ist ein strukturierter Wissens-Container, der Artikel organisiert und für semantische Suche verfügbar macht.

## Endpoints

```
GET  https://api.paperoffice.ai/latest/knowledge/kb_list
POST https://api.paperoffice.ai/latest/knowledge/kb_create
POST https://api.paperoffice.ai/latest/knowledge/kb_update
POST https://api.paperoffice.ai/latest/knowledge/kb_delete

POST https://api.paperoffice.ai/latest/knowledge/article_create
GET  https://api.paperoffice.ai/latest/knowledge/article_list
POST https://api.paperoffice.ai/latest/knowledge/article_update
POST https://api.paperoffice.ai/latest/knowledge/article_delete
```

**Authentifizierung:** Bearer Token für alle Endpoints.

## Parameter

### Knowledge Base

| Endpoint | Parameter | Typ | Pflicht | Beschreibung |
|---|---|---|---|---|
| `kb_create` | `name` | string | ✅ | Name der Knowledge Base |
| | `description` | string | ❌ | Beschreibung |
| | `visibility` | string | ❌ | Sichtbarkeit |
| | `primary_language` | string | ❌ | Sprache (z.B. `de`, `en`) |
| `kb_update` | `kb_id` | int | ✅ | ID der KB |
| | `name` | string | ❌ | Neuer Name |
| | `description` | string | ❌ | Neue Beschreibung |
| `kb_delete` | `kb_id` | int | ✅ | ID der zu löschenden KB |

### Artikel

| Endpoint | Parameter | Typ | Pflicht | Beschreibung |
|---|---|---|---|---|
| `article_create` | `kb_id` | int | ✅ | ID der Ziel-KB |
| | `title` | string | ✅ | Titel des Artikels |
| | `content` | string | ✅ | Inhalt |
| | `category` | string | ❌ | Kategorie |
| `article_list` | `kb_id` | int | ✅ | KB-ID (Query-Parameter) |
| `article_update` | `article_id` | int | ✅ | ID des Artikels |
| | `title` | string | ❌ | Neuer Titel |
| | `content` | string | ❌ | Neuer Inhalt |
| `article_delete` | `article_id` | int | ✅ | ID des zu löschenden Artikels |

## Ausführen

```bash
export PAPEROFFICE_API_KEY=po_sk_xxx

# Bash — KB erstellen, Artikel hinzufügen, auflisten, aufräumen
bash example.sh

# Python — Vollständiger CRUD-Zyklus mit allen Operationen
pip install requests
python3 example.py

# Node.js (v18+) — CRUD mit async/await
node example.js
```

## Erwartete Antwort (kb_list)

```json
{
    "status": "success",
    "count": 1,
    "data": [
        {
            "id": 9,
            "slug": "qa-kb-april6",
            "name": "QA-KB-April6",
            "status": "active"
        }
    ]
}
```

## Workflow

1. **KB erstellen** → `kb_create` gibt die neue KB mit ID zurück
2. **Artikel hinzufügen** → `article_create` mit `kb_id` als Referenz
3. **Artikel durchsuchen** → Siehe Recipe `kb-search/`
4. **Aktualisieren** → `kb_update` / `article_update` mit jeweiliger ID
5. **Löschen** → `kb_delete` entfernt KB inklusive aller Artikel

## Anwendungsfälle

- **Helpdesk:** FAQ-Artikel erstellen und für KI-Agenten durchsuchbar machen
- **Onboarding:** Wissensdatenbank mit Schulungsmaterial aufbauen
- **Produktdokumentation:** API-Referenzen und Guides zentral verwalten
- **Internes Wiki:** Abteilungswissen strukturiert ablegen und pflegen
