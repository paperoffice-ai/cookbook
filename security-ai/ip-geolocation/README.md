# IP Geolocation — Location & Device Data

Retrieves the physical location, device information, and exchange rates for an IP address. Without the IP parameter, the caller's own IP is used.

## Endpoint

```
POST https://api.paperoffice.ai/latest/ip2location/full
```

**Authentication:** VISITOR-capable (IP rate limit), recommended with Bearer token.

## Parameter

| Parameter | Type | Required | Description |
|---|---|---|---|
| `ip` | string | ❌ | IP address (default: own IP) |
| `locale` | string | ❌ | Response language (default: `de`) |

## How to run

```bash
export PAPEROFFICE_API_KEY=po_ut_xxx

# Bash — own IP
bash example.sh

# Bash — specific IP
bash example.sh "8.8.8.8"

# Python
pip install requests
python3 example.py "8.8.8.8"

# Node.js (v18+)
node example.js "8.8.8.8"
```

## Expected response (abbreviated)

```json
{
    "country": "DE",
    "country_name": "Deutschland",
    "city": "Frankfurt am Main",
    "latitude": 50.1109,
    "longitude": 8.6821,
    "timezone": "Europe/Berlin",
    "device": {
        "os": "Linux",
        "browser": "curl"
    },
    "exchange_rates": {
        "EUR": 1.0,
        "USD": 1.0862
    }
}
```

## Common use cases

- **Geo-blocking:** Restrict access to content by country
- **Fraud detection:** Compare IP location with billing address
- **Localization:** Automatically adapt language, currency, and tax rates
