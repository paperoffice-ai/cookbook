# Bildgenerierung

Erzeugt Bilder aus Text-Prompts mit dem PaperOffice ImageStudio. Drei Modell-Stufen für unterschiedliche Auflösungen. Automatische Prompt-Optimierung durch den integrierten Precompiler.

## Voraussetzungen

```bash
export PAPEROFFICE_API_KEY=po_sk_xxx
```

## Quick Start

```bash
# cURL
bash example.sh "A sunset over mountains" premium 1

# Python (benötigt: pip install requests)
python example.py "A sunset over mountains" premium 2

# Node.js 18+
node example.js "A sunset over mountains" premium 1
```

## Endpoint

```
POST https://api.paperoffice.ai/latest/job/add/paperoffice_imagestudio___generate
```

## Parameter

| Parameter | Typ | Pflicht | Default | Beschreibung |
|---|---|---|---|---|
| `prompt` | string | ✅ | — | Bildbeschreibung (auf Englisch empfohlen) |
| `model` | string | — | `basic` | Modell-Stufe (siehe Tabelle) |
| `num_images` | int | — | `1` | Anzahl zu generierender Bilder |
| `negative_prompt` | string | — | — | Unerwünschte Elemente ausschließen |
| `seed` | int | — | `-1` | Seed für Reproduzierbarkeit (`-1` = zufällig) |
| `steps` | int | — | `15` | Inferenz-Schritte (mehr = detaillierter, langsamer) |
| `guidance_scale` | float | — | `4.0` | Prompt-Treue (höher = strikter) |
| `precompile_prompt` | bool | — | `true` | Automatische Prompt-Optimierung |
| `output` | string | — | `url` | `url`, `base64` oder `inline` |
| `priority` | int | — | — | `≥ 900` für synchrone Verarbeitung |

## Modell-Stufen

| Modell | Auflösung | Empfehlung |
|---|---|---|
| `basic` | 512×512 | Schnelle Vorschau, Prototyping |
| `premium` | 1280×1280 | Standard für die meisten Anwendungsfälle |
| `ultra` | 2048×2048 | Höchste Qualität, Druckmaterial |

## Response-Beispiel

```json
{
  "status": "success",
  "result": {
    "status": "completed",
    "image_urls": [
      "https://api.paperoffice.ai/latest/job/download/..."
    ],
    "output_mode": "url"
  }
}
```

## Bonus-Features

### Prompt-Precompiler

Mit `precompile_prompt=true` wird der Prompt automatisch durch den `paperoffice_image_precompiler` optimiert — bessere Ergebnisse ohne manuelles Prompt-Engineering.

### Hintergrund entfernen

```bash
curl -s -X POST "https://api.paperoffice.ai/latest/job/add/paperoffice_imagestudio___remove_bg" \
  -H "Authorization: Bearer $PAPEROFFICE_API_KEY" \
  -F "file_1=@bild.png" \
  -F "priority=900" | python3 -m json.tool
```

## Tipps

- **Prompt-Sprache:** Englische Prompts liefern in der Regel bessere Ergebnisse
- **Negative Prompts:** z.B. `"blurry, low quality, distorted"` verbessert die Bildqualität
- **Reproduzierbarkeit:** Gleicher `seed` + gleicher `prompt` = identisches Bild
- **Guidance Scale:** Werte zwischen 3.0–7.0 sind für die meisten Prompts optimal
