# Pro Tips

## Kanonische Endpoints

PaperOffice AI hat zwei Endpoint-Muster:

### 1. Job-basierte Endpoints (Dateiverarbeitung)

```bash
POST https://api.paperoffice.ai/latest/job/add/{pipeline}
```

| Pipeline | Zweck |
|---|---|
| `workflow` | IDP, PDF Split/Merge/Convert/Anonymize |
| `paperoffice_aiocr___generate` | AI-OCR |
| `paperoffice_voice___tts` | Text-to-Speech |
| `paperoffice_voice___stt` | Speech-to-Text |
| `paperoffice_imagestudio___generate` | Bildgenerierung |
| `paperoffice_imagestudio___remove_bg` | Hintergrund entfernen |

### 2. Dedizierte REST-Endpoints

| Endpoint | Zweck |
|---|---|
| `POST /translate/text` | Übersetzung |
| `GET /translate/languages` | Sprachliste |
| `POST /vat/validate` | USt-ID Prüfung |
| `GET /vat/rates` | EU-Steuersätze (GRATIS) |
| `POST /fakeemail/check` | Fake-Email-Erkennung |
| `POST /fingerprint/verify` | Device Fingerprint |
| `POST /geocoding/forward` | Adresse → Koordinaten |
| `POST /geocoding/reverse` | Koordinaten → Adresse |
| `POST /ip2location/full` | IP → Geolocation |
| `POST /ip2location/vpn` | VPN/Proxy-Erkennung |
| `POST /currency_exchange/get_rates` | Wechselkurse |
| `POST /location2weather` | Wetter (GRATIS) |
| `POST /documents/search` | DMS-Suche |
| `POST /documents/upload` | DMS-Upload |
| `GET /webhooks/list` | Webhook-Liste |
| `POST /webhooks/subscribe` | Webhook registrieren |
| `GET /knowledge/kb_list` | Knowledge Bases |
| `POST /knowledge/search` | KB-Suche |

---

## Sync vs Async

| Priority | Modus | SLA | Verwendung |
|---|---|---|---|
| `≥ 900` | **SYNC** | ~20s | Development & Testing |
| `800–899` | ASYNC | 1 min | Urgent async |
| `500–599` | ASYNC | 30 min | **Production default** |
| `0–399` | ASYNC | 12–72h | Batch / Background |

```python
# Entwicklung: Sofort-Ergebnis
data = {"priority": 900}

# Produktion: Kosteneffizient
data = {"priority": 500}
```

**Sync (priority ≥ 900):** Antwort enthält sofort das Ergebnis.
**Async (priority < 900):** Antwort enthält `job_id`, dann pollen:

```bash
# Status abfragen
curl -s "https://api.paperoffice.ai/latest/job/get/{job_id}" \
  -H "Authorization: Bearer $PAPEROFFICE_API_KEY"
```

---

## Credit-System

Jeder API-Call verbraucht Credits. Höhere Priority = höhere Kosten.

| Priority | Multiplier | Beispiel (10-Credit-Job) |
|---|---|---|
| 500 (default) | 1.0x | 10 Credits |
| 700 | ~1.16x | ~12 Credits |
| 900 (sync) | ~1.33x | ~13 Credits |

**Gratis-Endpoints** (keine Credits):
- `GET /vat/rates`
- `POST /location2weather`
- `GET /health`

---

## Response-Strukturen

### OCR

```python
result = response.json()["result"]
fulltext = result["output"]["summary"]["poaiocr_extracted_fulltext"]
pages = result["output"]["pages"]
page_1 = pages["00001"]
print(page_1["ocr_text"])
print(page_1["confidence_avg"])
print(page_1["language"]["primary"])
```

### IDP (Rechnungsextraktion)

```python
result = response.json()["result"]
fields = result["pages_idp"][0]["suggested_fields"]

invoice_nr = fields["_invoice_number"]["value"]         # "2024-001"
total = fields["_total_amount"]["value_raw"]             # "1469.06" (normalisiert)
vat = fields["_vat_amount"]["value_raw"]                 # "234.56"
confidence = fields["_total_amount"]["source_boxes_confidence"]  # "high"
```

### TTS

```python
result = response.json()["result"]
audio_url = result["audio_url"]
duration = result["audio_duration_seconds"]
voice = result["voice"]
```

### STT

```python
result = response.json()["result"]
text = result["text"]
language = result["language"]
duration = result["audio_duration_seconds"]
```

### Image Generation

```python
result = response.json()["result"]
image_urls = result["image_urls"]  # Array!
```

### Translation

```python
data = response.json()["data"]
translated = data["translation"]
source_lang = data["source_language"]
target_lang = data["target_language"]
characters = data["characters"]
```

---

## Beste TTS-Stimmen

| Sprache | Stimme | Qualität |
|---|---|---|
| Deutsch | **Nadja** | Sehr natürlich |
| Englisch | **Joanna** | Natürlich |
| Spanisch | **Lucia** | Natürlich |

```python
data = {
    "text": "Guten Tag!",
    "voice": "Nadja",
    "speed": "1.0",
    "output_format": "mp3",
    "output": "url",
    "priority": 900,
}
```

---

## Authentifizierung

**Bearer Token für fast alle Endpoints erforderlich.**

```bash
export PAPEROFFICE_API_KEY="po_sk_xxx"

curl -X POST "https://api.paperoffice.ai/latest/..." \
  -H "Authorization: Bearer $PAPEROFFICE_API_KEY"
```

| Token-Typ | Prefix | Verwendung |
|---|---|---|
| System Key | `po_sk_` | Server-to-Server, voller Zugriff |
| User Token | `po_ut_` | User-scoped, abhängig von Lizenz |

**VISITOR-Mode** (kein Token): Nur `GET /health`, `/ip2location/*`, `/currency_exchange/*`, `GET /vat/rates`.

---

## MCP Integration

| Client | URL |
|---|---|
| Cursor IDE | `https://mcp.paperoffice.ai/cursor` |
| Claude Desktop | `https://mcp.paperoffice.ai/claude` |
| ChatGPT / OpenAI | `https://mcp.paperoffice.ai/openai` |
| Standard MCP | `https://mcp.paperoffice.ai/mcp` |
| Universal | `https://mcp.paperoffice.ai/` |

```json
{
  "mcpServers": {
    "paperoffice": {
      "url": "https://mcp.paperoffice.ai/cursor",
      "headers": {
        "Authorization": "Bearer YOUR_API_KEY"
      }
    }
  }
}
```

---

## Retry-Strategie (HTTP 429)

```python
import time
import requests

def api_call_with_retry(url, headers, data=None, files=None, max_retries=5):
    for attempt in range(max_retries):
        r = requests.post(url, headers=headers, data=data, files=files)
        if r.status_code != 429:
            return r
        wait = int(r.headers.get("Retry-After", 2 ** attempt))
        print(f"Rate limited, warte {wait}s...")
        time.sleep(wait)
    raise Exception("Rate limit nach {max_retries} Versuchen überschritten")
```

---

## VISITOR-Endpoints (kein Token)

Diese Endpoints funktionieren ohne Bearer Token (IP-basiertes Ratelimit):

| Endpoint | Limit |
|---|---|
| `GET /health` | Unbegrenzt |
| `POST /ip2location/full` | ~100 Requests/Tag |
| `POST /ip2location/vpn` | ~100 Requests/Tag |
| `POST /currency_exchange/get_rates` | ~100 Requests/Tag |
| `GET /vat/rates` | Gratis, unbegrenzt |

> **Empfehlung:** Auch für VISITOR-Endpoints einen Bearer Token verwenden, um IP-Ratelimits zu umgehen.

---

## Wichtige Parameter-Hinweise

| Parameter | Richtig | Falsch |
|---|---|---|
| STT Datei-Upload | `file_1` | `file` |
| Fingerprint ID | `visitorId` | `fingerprint_id` |
| DMS Suche | `global_search` | `search_query` |
| Image Gen Breite | `width` | `size` |
| Weather Koordinaten | `lat` + `lon` | `city` |
| Workspace | `workspace_name` | `metadata` |
