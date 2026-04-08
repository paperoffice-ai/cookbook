# Workspace erstellen & verwalten

Workspaces sind die oberste Organisationsebene im PaperOffice DMS. Jeder Workspace bildet einen **isolierten Dokumentenbereich** mit eigenen Berechtigungen und Suchindizes.

## Endpoints

| Aktion    | Methode | Pfad                                |
|-----------|---------|-------------------------------------|
| Erstellen | POST    | `/documents/workspace_create`       |
| Auflisten | GET     | `/documents/workspace_list`         |

**Authentifizierung:** Bearer Token (API-Key erforderlich)

## Parameter (Erstellen)

| Parameter     | Pflicht | Beschreibung                        |
|---------------|---------|-------------------------------------|
| `name`        | Ja      | Name des Workspace                  |
| `description` | Nein    | Optionale Beschreibung              |

## Ausführen

```bash
export PAPEROFFICE_API_KEY="dein_api_key"

# Bash
bash example.sh "Buchhaltung" "Rechnungen und Belege"

# Python
pip install requests
python3 example.py "Buchhaltung" "Rechnungen und Belege"

# Node.js
node example.js "Buchhaltung" "Rechnungen und Belege"
```

## Response-Struktur (Erstellen)

```json
{
  "status": "success",
  "workspace": {
    "id": 42,
    "name": "Buchhaltung",
    "description": "Rechnungen und Belege",
    "created_at": "2026-04-08T10:30:00Z"
  }
}
```

## Response-Struktur (Auflisten)

```json
{
  "status": "success",
  "workspaces": [
    {
      "id": 42,
      "name": "Buchhaltung",
      "description": "Rechnungen und Belege"
    }
  ]
}
```

## Workspace-Konzept

- **Isolation**: Dokumente in einem Workspace sind nur innerhalb dieses Workspace suchbar
- **Berechtigungen**: Zugriff wird pro Workspace über API-Keys gesteuert
- **Tagging**: Innerhalb eines Workspace können Dokumente zusätzlich mit Tags organisiert werden
- **Suche**: Jeder Workspace hat einen eigenen Suchindex für schnelle Abfragen

## Tipps

- Workspace-Namen sollten eindeutig und beschreibend sein
- Einen Workspace pro Abteilung oder Projekt anlegen
- Über die Workspace-Liste regelmäßig prüfen, ob alle Workspaces noch benötigt werden
