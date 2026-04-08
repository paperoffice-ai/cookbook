# Fake Email Detection

Detects disposable email addresses (Mailinator, Guerrilla Mail, etc.), temporary domains, and suspicious patterns. Supports single and bulk checks (up to 100 emails).

## Endpoints

```
POST https://api.paperoffice.ai/latest/fakeemail/check
POST https://api.paperoffice.ai/latest/fakeemail/check_bulk
```

**Authentication:** Bearer token required.

## Parameter

| Parameter | Type | Required | Description |
|---|---|---|---|
| `email` | string | ✅ | Email address to check (single) |
| `emails` | array | ✅ | Up to 100 email addresses (bulk) |

## How to run

```bash
export PAPEROFFICE_API_KEY=po_sk_xxx

# Bash
bash example.sh "test@mailinator.com"

# Python
pip install requests
python3 example.py "test@mailinator.com"

# Node.js (v18+)
node example.js "test@mailinator.com"
```

## Expected response

```json
{
    "result": {
        "email": "test@mailinator.com",
        "is_fake": true,
        "risk_score": 70,
        "risk_level": "HIGH",
        "detection_method": "HIGH_RISK_SCORE",
        "recommendation": "REJECT",
        "checks": {}
    }
}
```

## Risk levels

| Level | Score | Description |
|---|---|---|
| `LOW` | 0–30 | Probably legitimate |
| `MEDIUM` | 31–60 | Suspicious, manual review recommended |
| `HIGH` | 61–100 | Very likely fake/disposable address |

## Common use cases

- **Registration:** Block disposable addresses during account creation
- **Newsletter:** List hygiene — filter out fake addresses before sending
- **Lead qualification:** Only process leads with real email addresses
