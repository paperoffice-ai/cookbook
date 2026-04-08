# Webhooks — Event Notifications

Instead of constantly polling the job status, you can register webhooks and get actively notified when an event occurs.

## Endpoints

| Action    | Method | Endpoint              |
|-----------|--------|-----------------------|
| Subscribe | POST   | `/webhooks/subscribe` |
| List      | GET    | `/webhooks/list`      |
| Test      | POST   | `/webhooks/test`      |

**Authentication:** Bearer Token for all endpoints

## Subscribe parameters

```json
{
  "name": "my_first_webhook",
  "url": "https://my-server.com/webhook",
  "events": ["job.completed", "job.failed"],
  "secret": "my_secret_key"
}
```

| Parameter | Required | Description                              |
|----------|----------|------------------------------------------|
| `name`   | Yes      | Unique name for the webhook              |
| `url`    | Yes      | HTTPS URL to be called                   |
| `events` | Yes      | Array of event types                     |
| `secret` | No       | Shared secret for signature verification |
| `filters`| No       | Additional filters (e.g. by tool ID)     |

## Available events

| Event            | Description                     |
|-----------------|---------------------------------|
| `job.completed` | Job completed successfully      |
| `job.failed`    | Job failed                      |
| `job.queued`    | Job added to the queue          |

## Signature verification

Every webhook call includes an `X-PaperOffice-Signature` header. Use it to verify that the call actually comes from PaperOffice:

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
python3 example.py serve                              # Start receiver

# Node.js (v18+)
node example.js https://my-server.com/webhook   # Register only
node example.js serve                             # Start receiver
```

## Webhook vs. Polling

| Aspect      | Polling                      | Webhooks                       |
|-------------|------------------------------|--------------------------------|
| Latency     | Depends on interval          | Near real-time                 |
| Traffic     | Many unnecessary requests    | Only on actual events          |
| Complexity  | Easier to implement          | Requires public endpoint       |
| Reliability | Always (pull-based)          | Retry logic required           |
