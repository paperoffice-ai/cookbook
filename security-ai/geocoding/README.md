# Geocoding — Adresse ↔ Koordinaten

Wandelt Adressen in GPS-Koordinaten um (Forward) und Koordinaten zurück in Adressen (Reverse). Unterstützt mehrere Sprachen.

## Endpoints

```
POST https://api.paperoffice.ai/latest/geocoding/forward
POST https://api.paperoffice.ai/latest/geocoding/reverse
```

**Authentifizierung:** Bearer Token erforderlich.

## Parameter (Forward)

| Parameter | Typ | Pflicht | Beschreibung |
|---|---|---|---|
| `address` | string | ✅ | Adresse oder Ortsname |
| `lang` | string | ❌ | Sprache der Antwort (Standard: `de`) |

## Parameter (Reverse)

| Parameter | Typ | Pflicht | Beschreibung |
|---|---|---|---|
| `lat` | float | ✅ | Breitengrad |
| `lng` | float | ✅ | Längengrad |
| `lang` | string | ❌ | Sprache der Antwort (Standard: `de`) |

## Ausführen

```bash
export PAPEROFFICE_API_KEY=po_sk_xxx

# Bash
bash example.sh "Alexanderplatz 1, Berlin"

# Python
pip install requests
python3 example.py "Brandenburger Tor, Berlin"

# Node.js (v18+)
node example.js "Marienplatz, München"
```

## Erwartete Antwort (Forward)

```json
{
    "success": true,
    "found": true,
    "lat": 52.52,
    "lng": 13.41,
    "display_name": "Alexanderplatz, Mitte, Berlin, Deutschland",
    "address": {
        "road": "Alexanderplatz",
        "city": "Berlin",
        "country": "Deutschland"
    },
    "results": []
}
```

## Anwendungsfälle

- **Adressvalidierung:** Prüfen ob eine eingegebene Adresse existiert
- **Entfernungsberechnung:** Koordinaten für Distanz-Berechnungen ermitteln
- **Kartendarstellung:** Adressen auf Karten anzeigen
- **Lieferzonen:** Prüfen ob eine Adresse in ein bestimmtes Gebiet fällt
