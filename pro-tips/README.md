# Pro Tips

## API-Endpoint

**Alle Datei-basierten Jobs laufen über `/job/add/workflow`:**

```bash
POST https://api.paperoffice.ai/latest/job/add/workflow
```

TTS (Text-to-Speech) hat einen eigenen Endpoint:

```bash
POST https://api.paperoffice.ai/latest/voice/tts
```

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
data={"priority": 900}

# Produktion: Kosteneffizient
data={"priority": 500}
```

**Tipp:** `priority=900` für Dev, `priority=500` für Produktion. Höhere Priority = höhere Credit-Kosten.

---

## Response-Struktur

Alle Workflow-Responses folgen diesem Schema:

```json
{
  "status": "success",
  "job_id": "poai-job_900_...",
  "result": {
    "fulltext": "... extrahierter Text ...",
    "pages_idp": [{ "suggested_fields": { ... } }],
    "pages_aiocr": { "summary": { ... }, "pages": { ... } },
    "pages_images": ["https://..."],
    "steps": [{ "id": "ocr", "status": "completed", "duration_ms": 285 }],
    "total_steps": 2,
    "duration_ms": 3272
  },
  "timing": { "actual_ms": 3319, "performance": "57.1x faster than expected" }
}
```

---

## IDP-Felder (Source Boxes)

IDP-Responses enthalten `suggested_fields` mit `source_boxes` pro extrahiertem Feld:

```python
result = response.json()
idp_page = result["result"]["pages_idp"][0]
fields = idp_page["suggested_fields"]

invoice_number = fields["_invoice_number"]
print(invoice_number["value"])                    # "RE-2024-001"
print(invoice_number["source_boxes"])             # [...]
print(invoice_number["source_boxes_confidence"])  # "high"

total = fields["_total_amount"]
print(total["value"])  # 1234.56
```

Verfügbare Invoice-Felder: `_invoice_number`, `_invoice_date`, `_supplier_name`, `_customer_name`, `_total_amount`, `_net_amount`, `_vat_amount`, `_creditor_iban`, `_creditor_bic`, `_payment_due_date`, `_line_items` (Tabelle), etc.

---

## OCR-Text

```python
result = response.json()

# Volltext aller Seiten
fulltext = result["result"]["fulltext"]

# Pro Seite
pages = result["result"]["pages_aiocr"]["pages"]
page_1 = pages["00001"]
print(page_1["ocr_text"])
print(page_1["bounding_boxes"])
print(page_1["confidence_avg"])
```

---

## Beste TTS-Stimme

Für Deutsch: **Nadja** mit Speed 1.0 klingt am natürlichsten.

```python
data={
    "voice": "Nadja",
    "speed": "1.0",
    "output_format": "mp3",
    "output": "url",
    "priority": 900,
}
```

---

## Authentifizierung

**Bearer Token ist für fast alle Endpoints erforderlich.** Ohne Token → VISITOR-Session (nur `/ip2location`, `/currencyexchange`, `/health`, `/ping`).

```bash
export PAPEROFFICE_API_KEY=po_sk_xxx

# Token-Typen:
# po_sk_xxx — System Key (Server-to-Server, voller Zugriff)
# po_ut_xxx — User Token (User-scoped, abhängig von Lizenz)
```

---

## MCP Integration

PaperOffice bietet einen vollständigen MCP-Server für native AI-Tool-Integration.

| Client | MCP URL |
|---|---|
| Cursor IDE | `https://mcp.paperoffice.ai/cursor` |
| Claude Desktop | `https://mcp.paperoffice.ai/claude` |
| Standard MCP | `https://mcp.paperoffice.ai/mcp` |
| OpenAI / ChatGPT | `https://mcp.paperoffice.ai/openai` |

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

## Retry-Strategie

Bei HTTP 429 (Rate Limit): Exponential Backoff.

```python
import time
import requests

def api_call_with_retry(url, headers, max_retries=5):
    for attempt in range(max_retries):
        r = requests.post(url, headers=headers)
        if r.status_code != 429:
            return r
        wait = int(r.headers.get("Retry-After", 2 ** attempt))
        time.sleep(wait)
    raise Exception("Rate limit exceeded after retries")
```

---

## Credit-System

Jeder API-Call verbraucht Credits. Höhere Priority = höhere Kosten.

| Priority | Multiplier | 10-Credit-Job |
|---|---|---|
| 500 (default) | 1.0x | 10 Credits |
| 700 | ~1.16x | ~12 Credits |
| 900 (sync) | ~1.33x | ~13 Credits |

→ [Pricing Calculator](https://app.paperoffice.ai/en/pricing/calculator)
