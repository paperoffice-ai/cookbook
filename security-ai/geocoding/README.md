# Geocoding — Address ↔ Coordinates

Converts addresses into GPS coordinates (forward) and coordinates back into addresses (reverse). Supports multiple result languages.

## Endpoints

```
POST https://api.paperoffice.ai/latest/geocoding/forward
POST https://api.paperoffice.ai/latest/geocoding/reverse
```

**Authentication:** Bearer Token required

## Parameters (Forward)

| Parameter | Type | Required | Default | Description |
|---|---|---|---|---|
| `address` | string | **Yes** | — | Address, city name, or place name |
| `lang` | string | No | `de` | Response language (`en`, `de`, `fr`, `es`, etc.) |

## Parameters (Reverse)

| Parameter | Type | Required | Default | Description |
|---|---|---|---|---|
| `lat` | float | **Yes** | — | Latitude |
| `lng` | float | **Yes** | — | Longitude |
| `lang` | string | No | `de` | Response language |

## How to run

```bash
export PAPEROFFICE_API_KEY="your_api_key"

# Bash
chmod +x example.sh && ./example.sh "Berlin, Germany"

# Python
pip install requests
python3 example.py "Berlin, Germany"

# Node.js (v18+)
node example.js "Berlin, Germany"
```

## Response example (Forward)

```json
{
  "success": true,
  "found": true,
  "query": "Berlin, Germany",
  "lat": 52.5173885,
  "lng": 13.3951309,
  "display_name": "Berlin, Germany",
  "address": {
    "city": "Berlin",
    "ISO3166-2-lvl4": "DE-BE",
    "country": "Germany",
    "country_code": "de"
  },
  "results": [
    {
      "lat": 52.5173885,
      "lng": 13.3951309,
      "display_name": "Berlin, Germany",
      "type": "administrative",
      "importance": 0.513,
      "address": {
        "city": "Berlin",
        "country": "Germany",
        "country_code": "de"
      }
    }
  ]
}
```

> **Note:** `lat`/`lng` at the top level are the best match. The `results` array contains all matches ranked by importance.

## Response example (Reverse)

```json
{
  "success": true,
  "found": true,
  "lat": 52.5173885,
  "lng": 13.3951309,
  "display_name": "Berlin, Germany",
  "address": {
    "city": "Berlin",
    "country": "Germany",
    "country_code": "de"
  }
}
```

## Response when not found

```json
{
  "success": true,
  "found": false,
  "query": "xyznonexistent12345",
  "results": []
}
```

> When `found` is `false`, the `lat`/`lng` fields are absent and `results` is empty.

## Common use cases

- **Address validation:** Check whether an entered address exists
- **Distance calculation:** Determine coordinates for distance calculations
- **Map display:** Show addresses on maps
- **Delivery zones:** Check whether an address falls within a specific area

## See also

- [IP Geolocation](../ip-geolocation/) — Get location from IP address
- [Weather](../weather/) — Get weather for coordinates
