# Dokument hochladen (DMS Upload)

Lädt ein Dokument in das PaperOffice DMS hoch. Dokumente werden automatisch indexiert und sind sofort über die **Smart Search** auffindbar.

## Endpoint

```
POST https://api.paperoffice.ai/latest/documents/upload
```

**Authentifizierung:** Bearer Token (API-Key erforderlich)

## Parameter

| Parameter        | Pflicht | Beschreibung                                    |
|------------------|---------|-------------------------------------------------|
| `file_1`         | Ja      | Datei (PDF, DOCX, Bild, etc.)                   |
| `workspace_name` | Ja      | Ziel-Workspace für das Dokument                  |
| `tags`           | Nein    | Komma-getrennte Tags (z.B. "rechnung,2026,q1")  |
| `description`    | Nein    | Optionale Beschreibung des Dokuments             |

## Ausführen

```bash
export PAPEROFFICE_API_KEY="dein_api_key"

# Bash
bash example.sh vertrag.pdf "Buchhaltung" "vertrag,2026"

# Python
pip install requests
python3 example.py vertrag.pdf "Buchhaltung" "vertrag,2026"

# Node.js
npm install form-data
node example.js vertrag.pdf "Buchhaltung" "vertrag,2026"
```

## Response-Struktur

```json
{
  "status": "success",
  "document": {
    "id": 1234,
    "filename": "vertrag.pdf",
    "workspace": "Buchhaltung",
    "tags": ["vertrag", "2026"],
    "size": 245760,
    "created_at": "2026-04-08T10:30:00Z"
  }
}
```

## Upload-Workflow

1. **Workspace wählen** — Dokument einem bestehenden Workspace zuordnen
2. **Tags vergeben** — Komma-getrennte Tags für spätere Filterung
3. **Upload** — Datei wird hochgeladen und automatisch indexiert
4. **Suche** — Dokument ist sofort über Smart Search auffindbar

## Tagging-Strategie

Empfohlene Tag-Kategorien:

| Kategorie     | Beispiele                          |
|---------------|------------------------------------|
| Dokumenttyp   | `rechnung`, `vertrag`, `angebot`   |
| Zeitraum      | `2026`, `q1`, `januar`             |
| Abteilung     | `buchhaltung`, `hr`, `einkauf`     |
| Status        | `offen`, `geprüft`, `archiviert`   |
| Priorität     | `wichtig`, `dringend`              |

## Unterstützte Dateiformate

PDF, DOCX, DOC, XLSX, XLS, PPTX, PPT, TXT, CSV, PNG, JPG, TIFF, BMP, GIF, WEBP

## Tipps

- **Workspace vorher erstellen** — siehe Recipe `workspace-setup/`
- **Tags konsistent vergeben** — erleichtert spätere Suche erheblich
- **Dateigröße**: Maximal 50 MB pro Datei
- Nach dem Upload kann das Dokument sofort mit `document-chat/` befragt werden
