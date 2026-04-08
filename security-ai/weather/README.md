# Weather — Current Data & Forecast

Provides current weather data, multi-day forecast, and air quality for any GPS coordinates. **FREE** — costs no credits!

## Endpoint

```
POST https://api.paperoffice.ai/latest/location2weather
```

**Authentication:** Bearer token required, but **free** (no credit charge).

**Important:** Expects coordinates (`lat`/`lon`), NOT city names!

## Parameter

| Parameter | Type | Required | Description |
|---|---|---|---|
| `lat` | float | ✅ | Latitude (e.g. `52.52` for Berlin) |
| `lon` | float | ✅ | Longitude (e.g. `13.41` for Berlin) |
| `locale` | string | ❌ | Response language (default: `de`) |

## How to run

```bash
export PAPEROFFICE_API_KEY=po_sk_xxx

# Bash — Berlin
bash example.sh 52.52 13.41

# Bash — Munich
bash example.sh 48.14 11.58

# Python
pip install requests
python3 example.py 52.52 13.41

# Node.js (v18+)
node example.js 52.52 13.41
```

## Expected response (abbreviated)

```json
{
    "current": {
        "temp_c": 4.3,
        "condition": { "text": "Overcast" },
        "humidity": 65,
        "wind_kph": 12.5,
        "feelslike_c": 1.2
    },
    "forecast": [
        {
            "date": "2026-04-08",
            "day": {
                "maxtemp_c": 8.5,
                "mintemp_c": 2.1,
                "condition": { "text": "Partly cloudy" }
            }
        }
    ],
    "air_quality": {
        "pm2_5": 12.3,
        "pm10": 18.7
    }
}
```

## Tip: Coordinates not known?

Combine this recipe with the [Geocoding recipe](../geocoding/): First address → coordinates, then coordinates → weather.

## Common use cases

- **Logistics:** Automatically display weather warnings for delivery routes
- **Construction:** Plan and document weather-dependent work
- **Events:** Check weather at the venue in advance
- **Smart home:** Incorporate weather data into automations
