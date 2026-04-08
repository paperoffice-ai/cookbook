# Pro Tips

## Canonical Endpoints

PaperOffice AI has two endpoint patterns:

### 1. Job-based Endpoints (File Processing)

```bash
POST https://api.paperoffice.ai/latest/job/add/{pipeline}
```

| Pipeline | Purpose |
|---|---|
| `workflow` | IDP, PDF AI Split, Document Anonymize |
| `paperoffice_aiocr___generate` | AI-OCR |
| `paperoffice_voice___tts` | Text-to-Speech |
| `paperoffice_voice___stt` | Speech-to-Text |
| `paperoffice_imagestudio___generate` | Image Generation |
| `paperoffice_imagestudio___remove_bg` | Background Removal |
| `paperoffice_dataripper___office2pdf` | Office → PDF (native MS Office) |
| `paperoffice_dataripper___pdf2office` | PDF → Office (DOCX/XLSX/PPTX) |

### 2. Dedicated REST Endpoints

| Endpoint | Purpose |
|---|---|
| `POST /translate/text` | Translation |
| `GET /translate/languages` | Language List |
| `POST /vat/validate` | VAT ID Validation |
| `GET /vat/rates` | EU Tax Rates (FREE) |
| `POST /fakeemail/check` | Fake Email Detection |
| `POST /fingerprint/verify` | Device Fingerprint |
| `POST /geocoding/forward` | Address → Coordinates |
| `POST /geocoding/reverse` | Coordinates → Address |
| `POST /ip2location/full` | IP → Geolocation |
| `POST /ip2location/vpn` | VPN/Proxy Detection |
| `POST /currency_exchange/get_rates` | Exchange Rates |
| `POST /location2weather` | Weather (FREE) |
| `POST /documents/search` | DMS Search |
| `POST /documents/upload` | DMS Upload |
| `POST /documents/workspace_create` | Create Workspace |
| `GET /documents/workspace_list` | Workspace List |
| `GET /webhooks/list` | Webhook List |
| `POST /webhooks/subscribe` | Register Webhook |
| `GET /knowledge/kb_list` | Knowledge Bases |
| `POST /knowledge/search` | KB Search |

---

## Sync vs Async

| Priority | Mode | SLA | Usage |
|---|---|---|---|
| `≥ 900` | **SYNC** | ~20s | Development & Testing |
| `800–899` | ASYNC | 1 min | Urgent async |
| `500–599` | ASYNC | 30 min | **Production default** |
| `0–399` | ASYNC | 12–72h | Batch / Background |

```python
# Development: Instant result
data = {"priority": 900}

# Production: Cost-efficient
data = {"priority": 500}
```

**Sync (priority ≥ 900):** Response contains the result immediately.
**Async (priority < 900):** Response contains `job_id`, then poll:

```bash
# Check status
curl -s "https://api.paperoffice.ai/latest/job/get/{job_id}" \
  -H "Authorization: Bearer $PAPEROFFICE_API_KEY"
```

---

## Credit System

Every API call consumes credits. Higher priority = higher cost.

| Priority | Multiplier | Example (10-credit job) |
|---|---|---|
| 500 (default) | 1.0x | 10 Credits |
| 700 | ~1.16x | ~12 Credits |
| 900 (sync) | ~1.33x | ~13 Credits |

**Free endpoints** (no credits):
- `GET /vat/rates`
- `POST /location2weather`
- `GET /health`

---

## Response Structures

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

### IDP (Invoice Extraction)

```python
result = response.json()["result"]
fields = result["pages_idp"][0]["suggested_fields"]

invoice_nr = fields["_invoice_number"]["value"]         # "2024-001"
total = fields["_total_amount"]["value_raw"]             # "1469.06" (normalized)
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

## Best TTS Voices

| Language | Voice | Quality |
|---|---|---|
| German | **Nadja** | Very natural |
| English | **Joanna** | Natural |
| Spanish | **Lucia** | Natural |

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

## Authentication

**Bearer token required for almost all endpoints.**

```bash
export PAPEROFFICE_API_KEY="po_sk_xxx"

curl -X POST "https://api.paperoffice.ai/latest/..." \
  -H "Authorization: Bearer $PAPEROFFICE_API_KEY"
```

| Token Type | Prefix | Usage |
|---|---|---|
| System Key | `po_sk_` | Server-to-server, full access |
| User Token | `po_ut_` | User-scoped, depends on license |

**VISITOR Mode** (no token): Only `GET /health`, `/ip2location/*`, `/currency_exchange/*`, `GET /vat/rates`.

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

## Retry Strategy (HTTP 429)

```python
import time
import requests

def api_call_with_retry(url, headers, data=None, files=None, max_retries=5):
    for attempt in range(max_retries):
        r = requests.post(url, headers=headers, data=data, files=files)
        if r.status_code != 429:
            return r
        wait = int(r.headers.get("Retry-After", 2 ** attempt))
        print(f"Rate limited, waiting {wait}s...")
        time.sleep(wait)
    raise Exception(f"Rate limit exceeded after {max_retries} attempts")
```

---

## VISITOR Endpoints (no token)

These endpoints work without a Bearer token (IP-based rate limit):

| Endpoint | Limit |
|---|---|
| `GET /health` | Unlimited |
| `POST /ip2location/full` | ~100 Requests/day |
| `POST /ip2location/vpn` | ~100 Requests/day |
| `POST /currency_exchange/get_rates` | ~100 Requests/day |
| `GET /vat/rates` | Free, unlimited |

> **Recommendation:** Use a Bearer token even for VISITOR endpoints to bypass IP rate limits.

---

## Important Parameter Notes

| Parameter | Correct | Incorrect |
|---|---|---|
| STT File Upload | `file_1` | `file` |
| Fingerprint ID | `visitorId` | `fingerprint_id` |
| DMS Search | `global_search` | `search_query` |
| Image Gen Size | `width`, `height` | `size` |
| Weather Coordinates | `lat` + `lon` | `city`, `lng` |
| Workspace | `workspace_name` | `metadata` |
