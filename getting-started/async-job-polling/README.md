# Async Job-Polling — Submit, Poll, Ergebnis

Für größere Dateien oder niedrigere Prioritäten arbeitet die PaperOffice AI API asynchron. Dieser Workflow zeigt den 3-Schritt-Prozess: Job einreichen → Status pollen → Ergebnis abholen.

## Endpoints

| Schritt  | Methode | Endpoint                                           |
|---------|---------|----------------------------------------------------|
| Submit  | POST    | `/job/add/paperoffice_aiocr___generate`             |
| Poll    | GET     | `/job/get/{job_id}`                                 |
| Download| GET     | `/job/download/{token}` (falls Datei-Ergebnis)      |

**Authentifizierung:** Bearer Token für alle Endpoints

## Sync vs. Async

Der Unterschied liegt in der `priority`:

| Priority | Modus        | Verhalten                                      |
|---------|--------------|-------------------------------------------------|
| `900`   | **Synchron** | Ergebnis direkt in der Response                  |
| `500`   | **Async**    | Gibt `job_id` zurück, Ergebnis muss gepollt werden |
| `100`   | **Niedrig**  | Hintergrund-Queue, längere Wartezeit             |

## Polling-Ablauf

```
POST /job/add/... (priority=500)
  └─→ {"status":"success", "job_id":"poai-job_500_abc123"}

GET /job/get/poai-job_500_abc123
  └─→ {"status":"processing"}     ← weiter pollen
  └─→ {"status":"queued"}         ← weiter pollen
  └─→ {"status":"completed", "result":{...}}  ← fertig!
```

## Ausführen

```bash
export PAPEROFFICE_API_KEY="dein_api_key"

# Bash
chmod +x example.sh && ./example.sh /pfad/zur/datei.pdf

# Python
pip install requests
python3 example.py /pfad/zur/datei.pdf

# Node.js (v18+)
node example.js /pfad/zur/datei.pdf
```

## Tipps

- **Polling-Intervall:** 2 Sekunden ist ein guter Startwert. Für große Dateien ggf. auf 5s erhöhen.
- **Timeout:** Nach 60 Sekunden abbrechen und den User informieren.
- **Webhooks:** Statt Polling kannst du auch Webhooks nutzen — siehe das `webhooks/` Recipe.
