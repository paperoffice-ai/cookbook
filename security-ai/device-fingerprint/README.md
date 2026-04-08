# Device Fingerprint — Device Verification

Checks whether a device (browser/app) is known and trusted. Ideal for fraud detection, account security, and multi-device tracking.

## Endpoint

```
POST https://api.paperoffice.ai/latest/fingerprint/verify
```

**Authentication:** Bearer token required.

## Parameter

| Parameter | Type | Required | Description |
|---|---|---|---|
| `visitorId` | string | ✅ | Unique device ID (e.g. from FingerprintJS) |

## How to run

```bash
export PAPEROFFICE_API_KEY=po_sk_xxx

# Bash
bash example.sh "visitor_abc123"

# Python
pip install requests
python3 example.py "visitor_abc123"

# Node.js (v18+)
node example.js "visitor_abc123"
```

## Expected response

```json
{
    "verified": false,
    "visitorId": "visitor_abc123",
    "reason": "unknown_device",
    "status": "success"
}
```

## Common use cases

- **Login protection:** Block unknown devices during sensitive actions or enforce 2FA
- **Fraud detection:** Detect suspicious device changes
- **Account sharing:** Detect when an account is used from too many devices
