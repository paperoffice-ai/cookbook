# Geocoding — Address ↔ Coordinates

Converts addresses into GPS coordinates (forward) and coordinates back into addresses (reverse). Supports multiple languages.

## Endpoints

```
POST https://api.paperoffice.ai/latest/geocoding/forward
POST https://api.paperoffice.ai/latest/geocoding/reverse
```

**Authentication:** Bearer token required.

## Parameter (Forward)

| Parameter | Type | Required | Description |
|---|---|---|---|
| `address` | string | ✅ | Address or place name |
| `lang` | string | ❌ | Response language (default: `de`) |

## Parameter (Reverse)

| Parameter | Type | Required | Description |
|---|---|---|---|
| `lat` | float | ✅ | Latitude |
| `lng` | float | ✅ | Longitude |
| `lang` | string | ❌ | Response language (default: `de`) |

## How to run

```bash
export PAPEROFFICE_API_KEY=po_sk_xxx

# Bash
bash example.sh "Times Square, New York"

# Python
pip install requests
python3 example.py "Central Park, New York"

# Node.js (v18+)
node example.js "Times Square, New York"
```

## Expected response (Forward)

```json
{
    "success": true,
    "found": true,
    "lat": 52.52,
    "lng": 13.41,
    "display_name": "Times Square, Manhattan, New York, USA",
    "address": {
        "road": "Broadway",
        "city": "New York",
        "country": "United States"
    },
    "results": []
}
```

## Common use cases

- **Address validation:** Check whether an entered address exists
- **Distance calculation:** Determine coordinates for distance calculations
- **Map display:** Show addresses on maps
- **Delivery zones:** Check whether an address falls within a specific area
