# VAT ID Validation

Validates European VAT identification numbers through three layers: format check, check digit, and VIES query. Includes fraud risk assessment and optional geocoding. EU tax rates available for free.

## Endpoints

```
POST https://api.paperoffice.ai/latest/vat/validate
GET  https://api.paperoffice.ai/latest/vat/rates      (FREE — no token required)
```

**Authentication:** Bearer Token required for `/vat/validate`. `/vat/rates` is free without token.

## Parameters (validate)

| Parameter | Type | Required | Default | Description |
|---|---|---|---|---|
| `vat_id` | string | **Yes** | — | VAT ID including country code (e.g. `IE6388047V`) |
| `ip` | string | No | — | IP address for additional geo plausibility check |
| `email` | string | No | — | Email for additional plausibility check |
| `force_recheck` | bool | No | `false` | Bypass cache, query VIES directly |
| `geocoding` | bool | No | `false` | Enable address geocoding |

## How to run

```bash
export PAPEROFFICE_API_KEY="your_api_key"

# Bash
chmod +x example.sh && ./example.sh "IE6388047V"

# Python
pip install requests
python3 example.py "IE6388047V"

# Node.js (v18+)
node example.js "IE6388047V"
```

## Response example (valid VAT ID)

```json
{
  "status": "success",
  "vat_id": "IE6388047V",
  "format_valid": true,
  "vies_valid": true,
  "company_name": "GOOGLE IRELAND LIMITED",
  "company_address": "3RD FLOOR, GORDON HOUSE, BARROW STREET, DUBLIN 4",
  "country_code": "IE",
  "tax_context": {
    "vat_rate_standard": 23,
    "vat_rate_reduced": 9,
    "currency": "EUR",
    "reverse_charge_applicable": true
  },
  "fraud_protection": {
    "score": 196,
    "max_score": 1000,
    "rating": "low_risk",
    "label": "Low Risk",
    "confidence": 0.78,
    "document_references": 377,
    "network_coverage": "global",
    "signals": {
      "country_risk": 92,
      "corruption_index": 65,
      "eppo_density": 5
    },
    "powered_by": "PaperOffice Global Document Intelligence"
  },
  "layer": "L3_vies",
  "processing_time_ms": 452
}
```

## Response example (invalid VAT ID)

```json
{
  "status": "error",
  "vat_id": "DE123456789",
  "format_valid": false,
  "error": "INVALID_CHECKSUM",
  "message": "Pruefziffer ungueltig",
  "layer": "L1_format",
  "processing_time_ms": 0
}
```

## Response example (rates — free)

```json
{
  "DE": { "standard": 19, "reduced": 7 },
  "AT": { "standard": 20, "reduced": 10 },
  "FR": { "standard": 20, "reduced": 5.5 },
  "IE": { "standard": 23, "reduced": 9 }
}
```

## Validation layers

| Layer | Description | Details |
|---|---|---|
| `L1_format` | Format & check digit | Offline check — instant, no network call |
| `L2_vies` | VIES database query | Real-time query to EU Commission database |
| `L3_enrichment` | Address + fraud assessment | Company data, fraud score, geocoding |

## Fraud protection scores

| Rating | Score range | Description |
|---|---|---|
| `low_risk` | 0–299 | Legitimate, well-known company |
| `medium_risk` | 300–599 | Some risk signals, review recommended |
| `high_risk` | 600–1000 | Significant fraud indicators |

## Common use cases

- **E-commerce:** Validate VAT ID at checkout, apply correct tax rates
- **Invoicing:** Automatically apply reverse charge procedure for EU B2B
- **Compliance:** Document VAT ID checks for tax audits
- **Fraud prevention:** Detect shell companies via fraud protection score

## See also

- [Fake Email Detection](../fake-email-detection/) — Detect disposable emails
- [Device Fingerprint](../device-fingerprint/) — Identify repeat visitors
