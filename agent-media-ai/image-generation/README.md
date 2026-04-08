# Image Generation

Generates images from text prompts with PaperOffice ImageStudio. Three model tiers for different resolutions. Automatic prompt optimization via the built-in precompiler.

## Prerequisites

```bash
export PAPEROFFICE_API_KEY=po_sk_xxx
```

## Quick Start

```bash
# cURL
bash example.sh "A sunset over mountains" premium 1

# Python (requires: pip install requests)
python example.py "A sunset over mountains" premium 2

# Node.js 18+
node example.js "A sunset over mountains" premium 1
```

## Endpoint

```
POST https://api.paperoffice.ai/latest/job/add/paperoffice_imagestudio___generate
```

## Parameters

| Parameter | Type | Required | Default | Description |
|---|---|---|---|---|
| `prompt` | string | ✅ | — | Image description (English recommended) |
| `model` | string | — | `basic` | Model tier (see table) |
| `num_images` | int | — | `1` | Number of images to generate |
| `negative_prompt` | string | — | — | Exclude unwanted elements |
| `seed` | int | — | `-1` | Seed for reproducibility (`-1` = random) |
| `steps` | int | — | `15` | Inference steps (more = more detailed, slower) |
| `guidance_scale` | float | — | `4.0` | Prompt adherence (higher = stricter) |
| `precompile_prompt` | bool | — | `true` | Automatic prompt optimization |
| `output` | string | — | `url` | `url`, `base64` or `inline` |
| `priority` | int | — | — | `≥ 900` for synchronous processing |

## Model Tiers

| Model | Resolution | Recommendation |
|---|---|---|
| `basic` | 512×512 | Quick preview, prototyping |
| `premium` | 1280×1280 | Standard for most use cases |
| `ultra` | 2048×2048 | Highest quality, print material |

## Response Example

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

## Bonus Features

### Prompt Precompiler

With `precompile_prompt=true` the prompt is automatically optimized by the `paperoffice_image_precompiler` — better results without manual prompt engineering.

### Remove Background

```bash
curl -s -X POST "https://api.paperoffice.ai/latest/job/add/paperoffice_imagestudio___remove_bg" \
  -H "Authorization: Bearer $PAPEROFFICE_API_KEY" \
  -F "file_1=@image.png" \
  -F "priority=900" | python3 -m json.tool
```

## Tips

- **Prompt language:** English prompts generally yield better results
- **Negative prompts:** e.g. `"blurry, low quality, distorted"` improves image quality
- **Reproducibility:** Same `seed` + same `prompt` = identical image
- **Guidance scale:** Values between 3.0–7.0 are optimal for most prompts
