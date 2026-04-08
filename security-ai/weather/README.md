# Wetter — Aktuelle Daten & Vorhersage

Liefert aktuelle Wetterdaten, Mehrtages-Vorhersage und Luftqualität für beliebige GPS-Koordinaten. **GRATIS** — kostet keine Credits!

## Endpoint

```
POST https://api.paperoffice.ai/latest/location2weather
```

**Authentifizierung:** Bearer Token erforderlich, aber **kostenlos** (keine Credit-Belastung).

**Wichtig:** Erwartet Koordinaten (`lat`/`lon`), NICHT Städtenamen!

## Parameter

| Parameter | Typ | Pflicht | Beschreibung |
|---|---|---|---|
| `lat` | float | ✅ | Breitengrad (z.B. `52.52` für Berlin) |
| `lon` | float | ✅ | Längengrad (z.B. `13.41` für Berlin) |
| `locale` | string | ❌ | Sprache der Antwort (Standard: `de`) |

## Ausführen

```bash
export PAPEROFFICE_API_KEY=po_sk_xxx

# Bash — Berlin
bash example.sh 52.52 13.41

# Bash — München
bash example.sh 48.14 11.58

# Python
pip install requests
python3 example.py 52.52 13.41

# Node.js (v18+)
node example.js 52.52 13.41
```

## Erwartete Antwort (gekürzt)

```json
{
    "current": {
        "temp_c": 4.3,
        "condition": { "text": "Bedeckt" },
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
                "condition": { "text": "Teilweise bewölkt" }
            }
        }
    ],
    "air_quality": {
        "pm2_5": 12.3,
        "pm10": 18.7
    }
}
```

## Tipp: Koordinaten nicht bekannt?

Kombiniere dieses Recipe mit dem [Geocoding-Recipe](../geocoding/): Erst Adresse → Koordinaten, dann Koordinaten → Wetter.

## Anwendungsfälle

- **Logistik:** Wetterwarnungen für Lieferrouten automatisch einblenden
- **Bauwirtschaft:** Wetterabhängige Arbeiten planen und dokumentieren
- **Events:** Wetter am Veranstaltungsort vorab prüfen
- **Smart Home:** Wetterdaten in Automatisierungen einbeziehen
