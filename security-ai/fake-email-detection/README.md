# Fake Email Detection

Detects disposable email addresses (Mailinator, Guerrilla Mail, etc.), temporary domains, and suspicious patterns. Supports single checks and bulk checks (up to 100 emails).

## Endpoints

```
POST https://api.paperoffice.ai/latest/fakeemail/check        (single)
POST https://api.paperoffice.ai/latest/fakeemail/check_bulk   (bulk)
```

**Authentication:** Bearer Token required

## Parameters (single check)

| Parameter | Type | Required | Default | Description |
|---|---|---|---|---|
| `email` | string | **Yes** | — | Email address to check |

## Parameters (bulk check)

| Parameter | Type | Required | Default | Description |
|---|---|---|---|---|
| `emails` | array | **Yes** | — | Array of up to 100 email addresses |

> **Note:** Use `email` (singular) for `/check` and `emails` (array) for `/check_bulk`. They are separate endpoints with separate parameters.

## How to run

```bash
export PAPEROFFICE_API_KEY="your_api_key"

# Bash
chmod +x example.sh && ./example.sh "test@mailinator.com"

# Python
pip install requests
python3 example.py "test@mailinator.com"

# Node.js (v18+)
node example.js "test@mailinator.com"
```

## Response example (single)

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

## Response example (bulk)

```json
{
  "results": [
    {
      "email": "test@mailinator.com",
      "is_fake": true,
      "risk_score": 70,
      "risk_level": "HIGH",
      "recommendation": "REJECT"
    },
    {
      "email": "real@company.com",
      "is_fake": false,
      "risk_score": 10,
      "risk_level": "LOW",
      "recommendation": "ALLOW"
    }
  ]
}
```

## Risk levels

| Level | Score | Recommendation | Description |
|---|---|---|---|
| `LOW` | 0–30 | `ALLOW` | Probably legitimate |
| `MEDIUM` | 31–60 | `REVIEW` | Suspicious, manual review recommended |
| `HIGH` | 61–100 | `REJECT` | Very likely fake/disposable address |

## Common use cases

- **Registration:** Block disposable addresses during account creation
- **Newsletter:** List hygiene — filter out fake addresses before sending
- **Lead qualification:** Only process leads with real email addresses
- **Form spam:** Prevent bot submissions using throwaway emails

## See also

- [VAT Validation](../vat-validation/) — Validate business legitimacy
- [Device Fingerprint](../device-fingerprint/) — Identify repeat visitors
