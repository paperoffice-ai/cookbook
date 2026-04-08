# Webhooks — Event Notifications

Instead of constantly polling the job status, you can register webhooks and get actively notified when an event occurs.

## Endpoints

| Action | Method | Endpoint |
|---|---|---|
| Subscribe | POST | `/webhooks/subscribe` |
| List | GET | `/webhooks/list` |
| Update | POST | `/webhooks/update` |
| Delete | POST | `/webhooks/delete` |
| Test | POST | `/webhooks/test` |
| Deliveries | GET | `/webhooks/deliveries` |
| Info | GET | `/webhooks/info` |

**Authentication:** Bearer Token for all endpoints

## Subscribe parameters

| Parameter | Type | Required | Default | Description |
|---|---|---|---|---|
| `name` | string | **Yes** | — | Unique name for the webhook |
| `url` | string | **Yes** | — | HTTPS URL to be called |
| `events` | array | **Yes** | — | Array of event types (or `["*"]` for all) |
| `secret` | string | No | auto-generated | Shared secret for HMAC signature verification |
| `filters` | object | No | — | Filter by `workspace_id`, `pofid`, etc. |
| `headers` | object | No | — | Additional HTTP headers as key-value pairs |
| `retry_policy` | string | No | `exponential` | `none`, `linear`, `exponential` |
| `max_retries` | int | No | `5` | Maximum retries (0–10) |
| `timeout_ms` | int | No | `10000` | Request timeout in ms (1000–30000) |

## Available events

| Event | Description |
|---|---|
| `job.completed` | Job completed successfully |
| `job.failed` | Job failed |
| `job.queued` | Job added to the queue |
| `document.created` | Document created in DMS |
| `*` | All events |

## Webhook delivery payload

When an event occurs, PaperOffice sends an HTTP POST to your URL:

```json
{
  "event": "job.completed",
  "timestamp": "2026-04-08T12:00:00.000Z",
  "subscription_id": 42,
  "data": {
    "job_id": "poai-job_500_abc123",
    "pipeline": "paperoffice_aiocr___generate",
    "status": "completed",
    "result": { }
  }
}
```

### Headers sent with each delivery

| Header | Description |
|---|---|
| `X-PaperOffice-Signature` | HMAC-SHA256 signature of the body |
| `X-PaperOffice-Event` | Event type (e.g. `job.completed`) |
| `Content-Type` | `application/json` |

## Signature verification

Verify that webhook calls actually come from PaperOffice:

```python
import hmac, hashlib

expected = hmac.new(
    secret.encode(),
    request_body,
    hashlib.sha256
).hexdigest()

is_valid = hmac.compare_digest(expected, received_signature)
```

## How to run

```bash
export PAPEROFFICE_API_KEY="your_api_key"

# Register webhook (Bash)
chmod +x example.sh && ./example.sh https://my-server.com/webhook

# Python — Register + start receiver
pip install requests flask
python3 example.py https://my-server.com/webhook   # Register only
python3 example.py serve                            # Start receiver

# Node.js (v18+)
node example.js https://my-server.com/webhook   # Register only
node example.js serve                           # Start receiver
```

## Test endpoint

Send a test event to verify your webhook is receiving correctly:

```bash
curl -X POST "https://api.paperoffice.ai/latest/webhooks/test" \
  -H "Authorization: Bearer $PAPEROFFICE_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"subscription_id": 42}'
```

## Webhook vs. Polling

| Aspect | Polling | Webhooks |
|---|---|---|
| Latency | Depends on interval | Near real-time |
| Traffic | Many unnecessary requests | Only on actual events |
| Complexity | Easier to implement | Requires public endpoint |
| Reliability | Always (pull-based) | Retry logic built-in |
| Best for | Dev/testing, simple scripts | Production, event-driven |

## See also

- [Async Job Polling](../async-job-polling/) — Alternative: poll instead of webhook
