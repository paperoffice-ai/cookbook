# Pro Tips

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

## Bounding Boxes

IDP-Responses enthalten `bbox` für jedes extrahierte Feld — ein Array `[x1, y1, x2, y2]` mit Pixel-Koordinaten.

```python
field = result["job_result"]["fields"]["vendor"]
print(field["value"])       # "Acme Corp"
print(field["bbox"])        # [120, 340, 450, 370]
print(field["confidence"])  # 0.97
```

Perfekt für Verification UIs: Feld im PDF highlighten, Confidence-basiertes Review.

---

## Beste TTS-Stimme

Für Deutsch: **Nadja** mit Speed 1.0 klingt am natürlichsten.

```python
data={
    "voice": "Nadja",
    "speed": "1.0",
    "output_format": "mp3",
    "output": "url",
    "priority": 999,   # TTS immer sync
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
