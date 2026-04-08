# VAT ID Validation — VAT Check

Validates European VAT identification numbers in multiple layers: format check, check digit, and VIES query. Additionally, EU tax rates can be fetched for free.

## Endpoints

```
POST https://api.paperoffice.ai/latest/vat/validate
GET  https://api.paperoffice.ai/latest/vat/rates    (FREE)
```

**Authentication:** Bearer token for `/vat/validate`. `/vat/rates` is free without token.

## Parameter (validate)

| Parameter | Type | Required | Description |
|---|---|---|---|
| `vat_id` | string | ✅ | VAT ID including country code (e.g. `DE123456789`) |
| `ip` | string | ❌ | IP for additional geo check |
| `email` | string | ❌ | Email for additional plausibility check |
| `force_recheck` | bool | ❌ | Bypass cache, check directly with VIES |
| `geocoding` | bool | ❌ | Enable address geocoding |

## How to run

```bash
export PAPEROFFICE_API_KEY=po_sk_xxx

# Bash
bash example.sh "DE123456789"

# Python
pip install requests
python3 example.py "DE123456789"

# Node.js (v18+)
node example.js "DE123456789"
```

## Expected response (validate)

```json
{
    "status": "error",
    "vat_id": "DE123456789",
    "format_valid": false,
    "error": "INVALID_CHECKSUM",
    "message": "Pruefziffer ungueltig",
    "layer": "L1_format"
}
```

## Expected response (rates)

```json
{
    "DE": { "standard": 19, "reduced": 7 },
    "AT": { "standard": 20, "reduced": 10 },
    "FR": { "standard": 20, "reduced": 5.5 }
}
```

## Validation layers

| Layer | Description |
|---|---|
| `L1_format` | Format and check digit validation |
| `L2_vies` | VIES database query (EU Commission) |
| `L3_enrichment` | Address matching, geo check |

## Common use cases

- **E-commerce:** Validate VAT ID at checkout, apply correct tax rates
- **Invoicing:** Automatically apply reverse charge procedure
- **Compliance:** Document VAT ID checks for tax audits
